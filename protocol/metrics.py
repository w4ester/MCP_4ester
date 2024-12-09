import time
from typing import Dict, Any

class Metrics:
    """Metrics collection for MCP Framework.
    In production, consider using Prometheus or other monitoring systems.
    """
    
    def __init__(self):
        """Initialize metrics storage."""
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        self.total_latency = 0
        self.start_time = time.time()
    
    def record_request(self, prompt: str, success: bool, duration: float) -> None:
        """Record metrics for a request.
        
        Args:
            prompt (str): The input prompt
            success (bool): Whether the request was successful
            duration (float): Request processing duration in seconds
        """
        self.request_count += 1
        if success:
            self.success_count += 1
        else:
            self.error_count += 1
        self.total_latency += duration
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current metrics.
        
        Returns:
            Dict[str, Any]: Dictionary of current metrics
        """
        uptime = time.time() - self.start_time
        avg_latency = self.total_latency / self.request_count if self.request_count > 0 else 0
        
        return {
            'uptime': uptime,
            'request_count': self.request_count,
            'success_count': self.success_count,
            'error_count': self.error_count,
            'success_rate': self.success_count / self.request_count if self.request_count > 0 else 0,
            'average_latency': avg_latency
        }
    
    def reset(self) -> None:
        """Reset all metrics."""
        self.__init__()