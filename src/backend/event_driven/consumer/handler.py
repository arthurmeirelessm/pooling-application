from typing import Dict, Any
from src.backend.event_driven.consumer.controller.consumer_controller import ConsumerController
import json
import re


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    controller = ConsumerController()
    return controller.handle_request(event)
