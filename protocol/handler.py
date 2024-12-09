import re
import json
from typing import Dict, Optional, Any
from .context import ContextLayers
from .caching import SimpleCache
from .metrics import Metrics
from policies.policy_checker import PolicyChecker

class ModelContextProtocolHandler:
    """Core MCP handler that processes requests through the protocol pipeline."""
    
    def __init__(self, settings: Any, tools: Dict[str, Any], model_clients: Dict[str, Any]):
        """Initialize the MCP handler.
        
        Args:
            settings: Configuration settings
            tools: Dictionary of available tools
            model_clients: Dictionary of available model clients
        """
        self.settings = settings
        self.tools = tools
        self.model_clients = model_clients
        self.cache = SimpleCache() if self.settings.enable_caching else None
        self.metrics = Metrics() if self.settings.enable_metrics else None
        self.policy_checker = PolicyChecker(self.settings.forbidden_phrases)
    
    def build_prompt(self, context: ContextLayers) -> str:
        """Build a complete prompt from context layers.
        
        Args:
            context (ContextLayers): Context layers to combine
            
        Returns:
            str: Complete prompt for the model
        """
        prompt_parts = []
        
        # Add system instructions
        for msg in context.system:
            prompt_parts.append(f"[SYSTEM] {msg}")
        
        # Add developer context
        for msg in context.developer:
            prompt_parts.append(f"[DEVELOPER] {msg}")
        
        # Add user input
        for msg in context.user:
            prompt_parts.append(f"[USER] {msg}")
        
        return "\n".join(prompt_parts)
    
    def extract_tool_requests(self, model_response: str) -> list:
        """Extract tool requests from model response.
        
        Args:
            model_response (str): Raw model response
            
        Returns:
            list: List of (tool_name, params_json) tuples
        """
        # Example pattern: TOOL:tool_name:{"param": "value"}
        pattern = r"TOOL:(\w+):({.*?})"
        return re.findall(pattern, model_response)
    
    async def run_tool(self, tool_name: str, params_str: str) -> str:
        """Execute a tool with given parameters.
        
        Args:
            tool_name (str): Name of the tool to run
            params_str (str): Tool parameters as JSON string
            
        Returns:
            str: Tool execution result
        """
        try:
            params = json.loads(params_str)
            tool = self.tools.get(tool_name)
            if not tool:
                return f"Error: tool {tool_name} not found."
            return tool(params)
        except Exception as e:
            return f"Error executing tool: {str(e)}"
    
    async def process_request(
        self,
        context: ContextLayers,
        model_name: Optional[str] = None
    ) -> str:
        """Process a request through the MCP pipeline.
        
        Args:
            context (ContextLayers): Request context
            model_name (Optional[str]): Name of model to use
            
        Returns:
            str: Model response after processing
        """
        prompt = self.build_prompt(context)
        
        # Check policies on user input
        if not self.policy_checker.check(prompt):
            return "Request violates system policies."
        
        # Check cache
        if self.cache:
            cached = self.cache.get(prompt)
            if cached:
                return cached
        
        # Select model
        model_key = model_name or self.settings.default_model
        model_client = self.model_clients.get(model_key)
        if not model_client:
            return f"Model {model_key} not configured."
        
        # Generate initial response
        response = await model_client.generate(
            prompt,
            max_tokens=self.settings.max_tokens,
            temperature=self.settings.temperature
        )
        
        # Check policies on response
        if not self.policy_checker.check(response):
            return "Response violates system policies."
        
        # Process tool requests
        tool_requests = self.extract_tool_requests(response)
        for tool_name, params_str in tool_requests:
            tool_result = await self.run_tool(tool_name, params_str)
            
            # Update context with tool result
            tool_context = ContextLayers(
                system=context.system,
                developer=context.developer + [f"Tool {tool_name} result: {tool_result}"],
                user=context.user
            )
            
            # Regenerate response with tool context
            prompt = self.build_prompt(tool_context)
            response = await model_client.generate(
                prompt,
                max_tokens=self.settings.max_tokens,
                temperature=self.settings.temperature
            )
        
        # Final policy check
        if not self.policy_checker.check(response):
            return "Final response violates system policies."
        
        # Cache result
        if self.cache:
            self.cache.set(prompt, response)
        
        # Record metrics
        if self.metrics:
            self.metrics.record_request(prompt=prompt, success=True, duration=0.0)
        
        return response