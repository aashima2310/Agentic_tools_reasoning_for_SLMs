"""
Generates varied practice tasks, each with a KNOWN correct answer where possible.
This is what lets the verifier later check the teacher model's work.
"""
import random
from Tools.Functions import calculator, get_weather, search, FAKE_DOCS

CITIES = ["Indore", "Delhi", "Mumbai", "Paris"]


def generate_calculator_tasks(n=20):
    tasks = []
    for _ in range(n):
        a = random.randint(1, 500)
        b = random.choice([random.randint(1, 100), round(random.uniform(0.05, 0.9), 2)])
        op = random.choice(["+", "-", "*"])
        expr = f"{a} {op} {b}"
        expected = calculator(expr)
        tasks.append({
            "question": f"What is {a} {op} {b}?",
            "tools_needed": ["calculator"],
            "expected_answer": str(expected),
        })
    return tasks


def generate_weather_tasks(n=10):
    tasks = []
    for _ in range(n):
        city = random.choice(CITIES)
        result = get_weather(city)
        tasks.append({
            "question": f"What's the weather like in {city} right now?",
            "tools_needed": ["get_weather"],
            "expected_answer": f"{result['temp_c']}",  # check temp appears in answer
        })
    return tasks


def generate_search_tasks(n=10):
    # Build questions directly from the fake doc topics so there's a clear right answer
    topic_questions = [
        ("When was IIT Indore established?", "2009"),
        ("Who released the Qwen3 model family?", "alibaba"),
        ("What does GRPO remove the need for?", "critic"),
        ("What does LoRA fine-tuning train instead of the full model?", "small set"),
        ("When was the Eiffel Tower completed?", "1889"),
    ]
    tasks = []
    for q, ans in topic_questions[:n]:
        tasks.append({
            "question": q,
            "tools_needed": ["search"],
            "expected_answer": ans,
        })
    return tasks


def generate_multi_tool_tasks(n=10):
    tasks = []
    for _ in range(n):
        city = random.choice(CITIES)
        pct = random.randint(5, 40)
        weather = get_weather(city)
        temp = weather["temp_c"]
        expected = calculator(f"{temp} * {pct} / 100")
        tasks.append({
            "question": f"What's the weather in {city}, and what is {pct}% of that temperature in Celsius?",
            "tools_needed": ["get_weather", "calculator"],
            "expected_answer": str(expected),
        })
    return tasks


def generate_no_tool_tasks(n=10):
    # Questions the model should answer WITHOUT calling any tool
    qs = [
        "What is the capital of France?",
        "How many days are in a week?",
        "What is 2 + 2?",  # trivially easy - teaches "don't over-call tools"
        "Say hello in a friendly way.",
        "What color do you get mixing blue and yellow?",
    ]
    return [{"question": q, "tools_needed": [], "expected_answer": None} for q in qs[:n]]


def generate_all_tasks():
    tasks = (
        generate_calculator_tasks(20)
        + generate_weather_tasks(10)
        + generate_search_tasks(5)
        + generate_multi_tool_tasks(10)
        + generate_no_tool_tasks(5)
    )
    random.shuffle(tasks)
    return tasks


if __name__ == "__main__":
    tasks = generate_all_tasks()
    print(f"Generated {len(tasks)} tasks")
    for t in tasks[:5]:
        print(t)