"""
The full data generation pipeline. Run this file directly.

generate tasks -> ask teacher to solve each -> verify final answer against
our known ground truth -> save only the ones that pass to a JSONL file.
"""
import json
import time
from Data_gen.task_generator import generate_all_tasks
from Data_gen.groq_caller import solve_task
from tools.Verifier import verify_trajectory

OUTPUT_FILE = "data/verified_trajectories.jsonl"


def run_pipeline():
    tasks = generate_all_tasks()
    print(f"Generated {len(tasks)} tasks. Solving with teacher model...")

    passed = 0
    failed = 0

    with open(OUTPUT_FILE, "w") as f:
        for i, task in enumerate(tasks):
            try:
                result = solve_task(task["question"])
            except Exception as e:
                print(f"[{i}] API error, skipping: {e}")
                failed += 1
                continue

            # verify: did the tool calls execute fine (guaranteed, since we ran them for
            # real), AND does the final answer match our known expected answer?
            ok, reason = verify_trajectory(
                tool_calls=result["tool_calls"],
                final_answer=result["final_answer"],
                expected_answer=task["expected_answer"],
            )

            if ok and result["final_answer"] is not None:
                record = {
                    "question": task["question"],
                    "tool_calls": result["tool_calls"],
                    "final_answer": result["final_answer"],
                    "tools_needed": task["tools_needed"],
                }
                f.write(json.dumps(record) + "\n")
                passed += 1
            else:
                failed += 1
                print(f"[{i}] REJECTED: {reason} | Q: {task['question']}")

            time.sleep(0.3)  # small delay to be gentle on rate limits

    print(f"\nDone. Passed: {passed}, Rejected: {failed}")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run_pipeline()
