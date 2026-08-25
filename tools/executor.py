from tools.schemas import TOOL_NAMES
from tools.functions import TOOL_FUNCTIONS


def execute_tool_call(tool_name: str, arguments: dict):
    """
    Returns: (success: bool, result_or_error)
    """
    if tool_name not in TOOL_NAMES:
        return False, f"Unknown tool: '{tool_name}' is not in the fixed tool set."

    fn = TOOL_FUNCTIONS[tool_name]
    try:
        result = fn(**arguments)
        return True, result
    except TypeError as e:
        return False, f"Bad arguments for '{tool_name}': {e}"
    except Exception as e:
        return False, f"Tool '{tool_name}' raised an error: {e}"


if __name__ == "__main__":
    print(execute_tool_call("calculator", {"expression": "240 * 0.15"}))
    print(execute_tool_call("search", {"query": "Qwen3 model sizes"}))
    print(execute_tool_call("get_weather", {"location": "Indore"}))
    print(execute_tool_call("made_up_tool", {"x": 1}))
