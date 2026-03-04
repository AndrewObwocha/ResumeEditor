"""
Event bus implementation supporting both synchronous and asynchronous handlers.
"""
import asyncio
import logging
from typing import Callable, List, Any

logger = logging.getLogger(__name__)


class EventBus:
    """Simple pub/sub event bus with async support."""
    
    def __init__(self):
        """Initialize the event bus with empty handler registry."""
        self.handlers: dict = {}
        logger.info("EventBus initialized")
    
    def subscribe(self, event_type: type, handler: Callable) -> None:
        """
        Subscribe a handler to an event type.
        
        Args:
            event_type: The event class to subscribe to
            handler: Callable handler (can be sync or async)
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        handler_name = getattr(handler, '__name__', str(handler))
        logger.debug(f"Subscribed {handler_name} to {event_type.__name__}")
    
    def publish(self, event: Any) -> None:
        """
        Publish an event to all subscribed handlers.
        Supports both sync and async handlers with error isolation.
        
        Args:
            event: Event instance to publish
        """
        event_type = type(event)
        logger.debug(f"Publishing event: {event_type.__name__}")
        
        if event_type not in self.handlers:
            logger.debug(f"No handlers registered for {event_type.__name__}")
            return
        
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                for handler in self.handlers[event_type]:
                    if asyncio.iscoroutinefunction(handler):
                        asyncio.create_task(self._handle_async(handler, event))
                    else:
                        self._handle_sync(handler, event)
            else:
                for handler in self.handlers[event_type]:
                    if asyncio.iscoroutinefunction(handler):
                        asyncio.run(self._handle_async(handler, event))
                    else:
                        self._handle_sync(handler, event)
        except RuntimeError:
            for handler in self.handlers[event_type]:
                if asyncio.iscoroutinefunction(handler):
                    asyncio.run(self._handle_async(handler, event))
                else:
                    self._handle_sync(handler, event)
    
    async def publish_async(self, event: Any) -> None:
        """
        Async version of publish that waits for all handlers to complete.
        Provides better error handling and ensures handlers run sequentially.
        
        Args:
            event: Event instance to publish
        """
        event_type = type(event)
        logger.debug(f"Publishing event (async): {event_type.__name__}")
        
        if event_type not in self.handlers:
            logger.debug(f"No handlers registered for {event_type.__name__}")
            return
        
        for handler in self.handlers[event_type]:
            if asyncio.iscoroutinefunction(handler):
                await self._handle_async(handler, event)
            else:
                self._handle_sync(handler, event)
    
    async def _handle_async(self, handler: Callable, event: Any) -> None:
        """
        Execute async handler with error isolation.
        
        Args:
            handler: Async handler function
            event: Event to pass to handler
        """
        try:
            await handler(event)
        except Exception as e:
            handler_name = getattr(handler, '__name__', str(handler))
            logger.error(f"Error in async handler {handler_name}: {e}", exc_info=True)
    
    def _handle_sync(self, handler: Callable, event: Any) -> None:
        """
        Execute sync handler with error isolation.
        
        Args:
            handler: Sync handler function
            event: Event to pass to handler
        """
        try:
            handler(event)
        except Exception as e:
            handler_name = getattr(handler, '__name__', str(handler))
            logger.error(f"Error in sync handler {handler_name}: {e}", exc_info=True)