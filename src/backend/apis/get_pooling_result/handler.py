from typing import Dict, Any
from src.backend.apis.get_pooling_result.controller.get_pooling_result_controller import GetPoolingResultController
import json
import re


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    controller = GetPoolingResultController()
    return controller.handle_request(event)
