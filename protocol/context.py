from dataclasses import dataclass, field
from typing import List

@dataclass
class ContextLayers:
    """Data structure for holding layered context.
    
    Attributes:
        system (List[str]): System-level instructions and constraints
        developer (List[str]): Developer-provided context and tools
        user (List[str]): User inputs and history
    """
    system: List[str] = field(default_factory=list)
    developer: List[str] = field(default_factory=list)
    user: List[str] = field(default_factory=list)
    
    def add_system_context(self, context: str) -> None:
        """Add system-level context.
        
        Args:
            context (str): System context to add
        """
        self.system.append(context)
    
    def add_developer_context(self, context: str) -> None:
        """Add developer-level context.
        
        Args:
            context (str): Developer context to add
        """
        self.developer.append(context)
    
    def add_user_context(self, context: str) -> None:
        """Add user-level context.
        
        Args:
            context (str): User context to add
        """
        self.user.append(context)
    
    def clear_user_context(self) -> None:
        """Clear user context history."""
        self.user.clear()