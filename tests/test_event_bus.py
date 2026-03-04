"""
Tests for event bus functionality.
"""
import asyncio
import pytest
from src.infra.event_bus import EventBus
from src.events.events import (
    ApplicationStartedEvent,
    JobDescriptionFetchedEvent,
    ApplicationErrorEvent
)


class TestEventBus:
    """Test EventBus synchronous and asynchronous handler support."""
    
    def test_subscribe_and_publish_sync(self):
        """Test basic synchronous event subscription and publishing."""
        bus = EventBus()
        received_events = []
        
        def handler(event):
            received_events.append(event)
        
        bus.subscribe(ApplicationStartedEvent, handler)
        event = ApplicationStartedEvent(timestamp="2026-03-03")
        bus.publish(event)
        
        assert len(received_events) == 1
        assert received_events[0] == event
    
    @pytest.mark.asyncio
    async def test_subscribe_and_publish_async(self):
        """Test asynchronous event subscription and publishing."""
        bus = EventBus()
        received_events = []
        
        async def async_handler(event):
            await asyncio.sleep(0.01)  # Simulate async work
            received_events.append(event)
        
        bus.subscribe(ApplicationStartedEvent, async_handler)
        event = ApplicationStartedEvent(timestamp="2026-03-03")
        await bus.publish_async(event)
        
        assert len(received_events) == 1
        assert received_events[0] == event
    
    @pytest.mark.asyncio
    async def test_multiple_handlers(self):
        """Test that multiple handlers receive the same event."""
        bus = EventBus()
        handler1_received = []
        handler2_received = []
        
        async def handler1(event):
            handler1_received.append(event)
        
        async def handler2(event):
            handler2_received.append(event)
        
        bus.subscribe(JobDescriptionFetchedEvent, handler1)
        bus.subscribe(JobDescriptionFetchedEvent, handler2)
        
        event = JobDescriptionFetchedEvent(
            source="manual",
            content="Test job description",
            length=100
        )
        await bus.publish_async(event)
        
        assert len(handler1_received) == 1
        assert len(handler2_received) == 1
        assert handler1_received[0] == event
        assert handler2_received[0] == event
    
    @pytest.mark.asyncio
    async def test_error_isolation(self):
        """Test that errors in one handler don't affect others."""
        bus = EventBus()
        successful_handler_called = []
        
        async def failing_handler(event):
            raise Exception("Handler failure")
        
        async def successful_handler(event):
            successful_handler_called.append(event)
        
        bus.subscribe(ApplicationStartedEvent, failing_handler)
        bus.subscribe(ApplicationStartedEvent, successful_handler)
        
        event = ApplicationStartedEvent(timestamp="2026-03-03")
        
        # Should not raise despite failing handler
        await bus.publish_async(event)
        
        # Successful handler should still be called
        assert len(successful_handler_called) == 1
    
    def test_no_handlers_registered(self):
        """Test publishing to event type with no handlers."""
        bus = EventBus()
        event = ApplicationErrorEvent(
            stage="test",
            error_message="Test error",
            timestamp="2026-03-03"
        )
        
        # Should not raise
        bus.publish(event)
