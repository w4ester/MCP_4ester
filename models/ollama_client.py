import asyncio
import subprocess
from .base_client import ModelClient

class OllamaClient(ModelClient):
    """Ollama local model client implementation."""
    
    def __init__(self, model_name: str):
        """Initialize the Ollama client.
        
        Args:
            model_name (str): Name of the Ollama model to use
        """
        self.model_name = model_name
    
    async def generate(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate a response using Ollama.
        
        Args:
            prompt (str): Input prompt
            max_tokens (int, optional): Maximum tokens to generate. Defaults to 1000.
            temperature (float, optional): Sampling temperature. Defaults to 0.7.
            
        Returns:
            str: Generated response
        """
        try:
            # Create the Ollama command
            cmd = ["ollama", "generate", "-m", self.model_name, prompt]
            
            # Run the command asynchronously
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Wait for the command to complete
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                return f"Error calling Ollama: {stderr.decode()}"
            
            return stdout.decode().strip()
            
        except Exception as e:
            return f"Error executing Ollama command: {str(e)}"
