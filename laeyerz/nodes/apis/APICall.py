import requests
from laeyerz.flow.Node import Node

class APICallNode(Node):
    """
    Generic HTTP API call node
    """

    def __init__(self, name="APICall"):
        super().__init__(name)

        # Declare inputs (IMPORTANT for graph + studio)
        self.inputs = [
            {
                "name": "url",
                "type": "string",
                "description": "API endpoint URL",
                "inputType": "input",
                "required": True
            },
            {
                "name": "method",
                "type": "string",
                "description": "HTTP method: GET, POST, PUT, DELETE",
                "inputType": "input",
                "default": "GET"
            },
            {
                "name": "headers",
                "type": "dict",
                "description": "HTTP headers",
                "inputType": "input",
                "default": {}
            },
            {
                "name": "params",
                "type": "dict",
                "description": "Query parameters",
                "inputType": "input",
                "default": {}
            },
            {
                "name": "body",
                "type": "dict",
                "description": "JSON request body",
                "inputType": "input",
                "default": None
            },
            {
                "name": "timeout",
                "type": "number",
                "description": "Request timeout (seconds)",
                "inputType": "input",
                "default": 30
            }
        ]

        # Declare outputs
        self.outputs = [
            {"name": "status_code", "type": "number"},
            {"name": "headers", "type": "dict"},
            {"name": "response", "type": "any"},
            {"name": "raw_text", "type": "string"}
        ]

    def call(self, url, method="GET", headers={}, params={}, body=None, timeout=30):
    
        try:
            resp = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=body,
                timeout=timeout
            )

            # Try JSON first, fallback to text
            try:
                parsed = resp.json()
            except ValueError:
                parsed = None

            return {
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "response": parsed,
                "raw_text": resp.text
            }

        except requests.RequestException as e:
            return {
                "status_code": -1,
                "headers": {},
                "response": None,
                "raw_text": str(e)
            }
