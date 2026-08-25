
import os
import json
from dotenv import load_dotenv
from groq import Groq
from tools.schemas import TOOLS
from tools.executor import execute_tool_call

load_dotenv()

key = os.environ.get("GROQ_API_KEY")
print("DEBUG - Key found:", repr(key[:10]) if key else "NOT FOUND AT ALL")
print("DEBUG - Key found:", repr(key), "LENGTH:", len(key) if key else 0)
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Change this if you find a different/better model available in your Groq account
TEACHER_MODEL = "qwen/qwen3.6-27b"
SYSTEM_PROMPT = (
    "You are a helpful assistant with access to tools. "
    "Use a tool only when you actually need it to answer correctly. "
    "If you don't need a tool, just answer directly. "
    "After getting a tool result, decide if you need another tool call "
    "or if you can now give the final answer."
)


def solve_task(question: str, max_steps: int = 4):
    """
    Runs the full loop: send question -> maybe get tool call -> execute for
    real -> send result back -> repeat -> final answer.

    Returns a dict: {"tool_calls": [...], "final_answer": "...", "raw_messages": [...]}
    This is the format our verifier expects.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    executed_calls = []  # what we'll hand to the verifier

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=TEACHER_MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.3,
        )
        msg = response.choices[0].message

        # Case 1: model wants to call a tool
        if msg.tool_calls:
            # append the assistant's tool-call message to the conversation
            messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [tc.model_dump() for tc in msg.tool_calls],
            })

            for tc in msg.tool_calls:
                tool_name = tc.function.name
                try:
                    arguments = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    arguments = {}

                # ACTUALLY execute it for real, using our own code, not trusting the model's claim
                success, real_result = execute_tool_call(tool_name, arguments)

                executed_calls.append({
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "claimed_result": str(real_result) if success else "ERROR",
                    # note: claimed_result == real_result by construction here,
                    # because WE are the ones running it and feeding it back.
                    # The teacher never gets a chance to lie about the result -
                    # this is actually a stronger setup than pure text generation.
                })

                # feed the REAL result back to the model, not anything the model "claimed"
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(real_result) if success else f"Error: {real_result}",
                })

        # Case 2: model gave a final answer, no more tool calls
        else:
            return {
                "tool_calls": executed_calls,
                "final_answer": msg.content,
                "raw_messages": messages,
            }

    # If we hit max_steps without a final answer, treat as failed/incomplete
    return {
        "tool_calls": executed_calls,
        "final_answer": None,
        "raw_messages": messages,
    }


if __name__ == "__main__":
    result = solve_task("What is 15% of 240, and is that number even or odd?")
    print(json.dumps(result, indent=2, default=str))
