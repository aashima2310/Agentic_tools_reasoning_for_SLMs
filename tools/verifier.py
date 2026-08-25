from tools.executor import execute_tool_call

def verify_trajectory(tool_calls: list, final_answer: str = None,
                       expected_answer=None, tools_needed=None):
    """
    tool_calls: list of dicts: {"tool_name": ..., "arguments": {...}, "claimed_result": ...}
    tools_needed: list of tool names the task actually requires (from task_generator).
                  [] means "no tool should be used at all".
    Returns: (passed: bool, reason: str)
    """
    used_tools = [c.get("tool_name") for c in tool_calls]

    # NEW: catch unnecessary tool use on no-tool tasks
    if tools_needed == [] and len(used_tools) > 0:
        return False, f"No tool was needed, but model called {used_tools}"

    # NEW: catch wrong-tool / missed-tool cases
    if tools_needed:
        if not set(tools_needed).issubset(set(used_tools)):
            return False, f"Expected tools {tools_needed}, model used {used_tools}"

    for i, step in enumerate(tool_calls):
        name = step.get("tool_name")
        args = step.get("arguments", {})
        claimed = step.get("claimed_result")
        success, real_result = execute_tool_call(name, args)
        if not success:
            return False, f"Step {i}: tool call failed for real: {real_result}"
        if str(real_result).strip().lower() != str(claimed).strip().lower():
            return False, (
                f"Step {i}: hallucinated result. "
                f"Teacher claimed '{claimed}', real result was '{real_result}'"
            )

    # NEW: no-tool tasks now actually get checked, and final_answer=None is caught for ALL tasks
    if final_answer is None:
        return False, "No final answer produced"
    if expected_answer is not None:
        if str(expected_answer).strip().lower() not in final_answer.strip().lower():
            return False, f"Final answer doesn't mention expected answer '{expected_answer}'"

    return True, "passed"
