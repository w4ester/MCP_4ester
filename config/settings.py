from dataclasses import dataclass, field
from typing import Dict, Callable, List, Optional

@dataclass
class MCPSettings:
    # Paths or keys for model API access
    openai_api_key: str = "YOUR-OPENAI-API-KEY"
    ollama_model_name: str = "your-ollama-model"  # E.g., "llama3.3"
    
    # Default policies
    policy_file: str = "policies/constitution.txt"
    
    # Default model to use if not specified
    default_model: str = "ollama"
    
    # Tools registry (name -> callable)
    tools: Dict[str, Callable] = field(default_factory=dict)
    
    # Basic configuration
    max_tokens: int = 1000
    temperature: float = 0.7
