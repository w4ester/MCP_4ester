import time
from typing import Any, Callable, Dict
from .metrics import Metrics

class RequestTrackingMiddleware:
    """Middleware for tracking requests and recording metrics."""
    
    def __init__(self, app: Any, metrics: Metrics):
        """Initialize the middleware.
        
        Args:
            app: The ASGI application
            metrics (Metrics): Metrics collector instance
        """
        self.app = app
        self.metrics = metrics
    
    async def __call__(self, scope: Dict, receive: Callable, send: Callable):
        """Process the request and record metrics.
        
        Args:
            scope (Dict): ASGI scope
            receive (Callable): ASGI receive function
            send (Callable): ASGI send function
        """
        if scope['type'] == 'http':
            start_time = time.time()
            
            # Call next handler
            try:
                await self.app(scope, receive, send)
                success = True
            except Exception:
                success = False
                raise
            finally:
                duration = time.time() - start_time
                self.metrics.record_request(
                    prompt=scope.get('path', ''),
                    success=success,
                    duration=duration
                )
        else:
            await self.app(scope, receive, send)