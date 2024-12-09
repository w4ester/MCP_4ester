from abc import ABC, abstractmethod

class ModelClient(ABC):
    """Abstract base class for model clients."""
    
    @abstractmethod
    async def generate(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate a response from the model.
        
        Args:
            prompt (str): The input prompt for the model
            max_tokens (int, optional): Maximum tokens to generate. Defaults to 1000.
            temperature (float, optional): Sampling temperature. Defaults to 0.7.
            
        Returns:
            str: The generated response
        """
        pass