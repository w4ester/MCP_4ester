import asyncio

from config.settings import MCPSettings
from models.openai_client import OpenAIClient
from models.ollama_client import OllamaClient
from tools.search_tool import search_tool
from tools.wiki_tool import wiki_tool
from protocol.context import ContextLayers
from protocol.handler import ModelContextProtocolHandler

async def main():
    """Main entry point for the MCP Framework demo."""
    
    # Load settings
    settings = MCPSettings()
    
    # Register tools
    tools = {
        "search": search_tool,
        "wiki": wiki_tool
    }
    
    # Register models
    model_clients = {
        "openai": OpenAIClient(api_key=settings.openai_api_key),
        "ollama": OllamaClient(model_name=settings.ollama_model_name)
    }
    
    # Create the MCP handler
    handler = ModelContextProtocolHandler(
        settings=settings,
        tools=tools,
        model_clients=model_clients
    )
    
    # Example context
    context = ContextLayers(
        system=["Follow the constitution and do not produce disallowed content."],
        developer=["If user requests a search, use the search tool."],
        user=["Hello! Can you tell me about penguins? Also, please search for 'Arctic animals'."]
    )
    
    # Process the request
    response = await handler.process_request(context)
    print("MCP Response:", response)

if __name__ == "__main__":
    asyncio.run(main())