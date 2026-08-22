TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluates a mathematical expression and returns the numeric result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A math expression, e.g. '15 * 0.2' or '36 % 2'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Searches a knowledge base and returns relevant text snippets. Use this for factual questions you don't already know the answer to.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of results to return (default 3)"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Returns current weather for a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g. 'Indore'"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_date",
            "description": "Returns today's date, or does simple date arithmetic (e.g. 'days between two dates').",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "'today' or 'days_between'"
                    },
                    "date1": {"type": "string", "description": "YYYY-MM-DD, only needed for days_between"},
                    "date2": {"type": "string", "description": "YYYY-MM-DD, only needed for days_between"}
                },
                "required": ["operation"]
            }
        }
    }
]

TOOL_NAMES = {t["function"]["name"] for t in TOOLS}