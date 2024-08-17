from typing import Dict, Any
from src.backend.apis.create_status.controller.create_status_contoller import CreateStatusController
import json
import re


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    controller = CreateStatusController()
    return controller.handle_request(event)
