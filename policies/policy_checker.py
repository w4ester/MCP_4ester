from typing import List

class PolicyChecker:
    """Checks responses or prompts against defined policies."""
    
    def __init__(self, forbidden_phrases: List[str]):
        """Initialize the policy checker.
        
        Args:
            forbidden_phrases (List[str]): List of phrases that are not allowed
        """
        self.forbidden_phrases = forbidden_phrases
    
    def check(self, text: str) -> bool:
        """Check if text follows all policies.
        
        Args:
            text (str): Text to check against policies
            
        Returns:
            bool: True if allowed, False if disallowed
        """
        # Basic check for forbidden phrases
        for phrase in self.forbidden_phrases:
            if phrase.lower() in text.lower():
                return False
        
        # Additional policy checks could be added here
        # For example:
        # - Content classification
        # - Regex patterns
        # - External API checks
        
        return True