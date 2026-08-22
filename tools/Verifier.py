from tools.executor import execute_tool_call

def verify_trajectory(tool_calls: list, final_answer: str = None, expected_answer=None):
    """
    tool_calls: list of dicts: {"tool_name": ..., "arguments": {...}, "claimed_result": ...}
    Returns: (passed: bool, reason: str)
    """
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

    # Check final answer against known ground truth, if we have one
    if expected_answer is not None and final_answer is not None:
        if str(expected_answer).strip().lower() not in final_answer.strip().lower():
            return False, f"Final answer doesn't mention expected answer '{expected_answer}'"

    return True, "passed"


if __name__ == "__main__":
    good = [
        {"tool_name": "calculator", "arguments": {"expression": "240 * 0.15"}, "claimed_result": "36.0"},
    ]
    print(verify_trajectory(good, final_answer="15% of 240 is 36.", expected_answer="36"))

    # A BAD trajectory - teacher hallucinated the result - should fail
    bad = [
        {"tool_name": "calculator", "arguments": {"expression": "240 * 0.15"}, "claimed_result": "35"},
    ]
    print(verify_trajectory(bad, final_answer="15% of 240 is 35.", expected_answer="36"))