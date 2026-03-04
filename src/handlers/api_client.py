import logging
import requests
from ..config import API_URL, HEADERS
from ..events import PayloadReadyEvent, APISuccessEvent, APIRequestFailedEvent

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.event_bus.subscribe(PayloadReadyEvent, self.send_request)
        logger.info("APIClient initialized")
    
    def _make_request(self, payload: dict):
        """Make HTTP POST request to Instacart API"""
        logger.info(f"Sending POST request to {API_URL}")
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    
    def send_request(self, event: PayloadReadyEvent):
        try:
            response = self._make_request(event.payload)
            logger.info(f"API request successful: {response}")
            self.event_bus.publish(APISuccessEvent(response))
        except Exception as e:
            logger.error(f"API request failed: {e}")
            self.event_bus.publish(APIRequestFailedEvent(str(e)))