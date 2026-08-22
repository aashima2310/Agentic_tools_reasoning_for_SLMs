
import datetime
import re

def calculator(expression: str):
    if not re.match(r'^[\d\s\.\+\-\*\/\%\(\)]+$', expression):
        raise ValueError(f"Unsafe or invalid expression: {expression}")
    try:
        return eval(expression, {"__builtins__": {}})
    except Exception as e:
        raise ValueError(f"Could not evaluate '{expression}': {e}")

FAKE_DOCS = [
    {"id": "d1", "text": "IIT Indore was established in 2009 and is located in Simrol, Madhya Pradesh."},
    {"id": "d2", "text": "The Qwen3 model family was released by Alibaba and includes sizes from 0.6B to 235B parameters."},
    {"id": "d3", "text": "GRPO (Group Relative Policy Optimization) removes the need for a separate critic model used in PPO."},
    {"id": "d4", "text": "LoRA fine-tuning trains a small set of additional weights instead of the full model, saving GPU memory."},
    {"id": "d5", "text": "The Eiffel Tower was completed in 1889 and is located in Paris, France."},
    {"id": "d6", "text": "Photosynthesis converts sunlight, water, and carbon dioxide into glucose and oxygen."},
    
    {"id": "d7", "text": "The Transformer architecture was introduced in the 2017 paper 'Attention Is All You Need' and is based primarily on attention mechanisms."},
    {"id": "d8", "text": "RAG stands for Retrieval-Augmented Generation. It combines information retrieval with language generation to provide relevant external context to a language model."},
    {"id": "d9", "text": "FAISS is a library developed by Meta AI for efficient similarity search and clustering of dense vectors."},
    {"id": "d10", "text": "Chroma is an open-source vector database commonly used to store and retrieve embeddings for AI and RAG applications."},
    
    {"id": "d11", "text": "Python is a high-level programming language widely used in machine learning, data science, web development, and automation."},
    {"id": "d12", "text": "PyTorch is an open-source deep learning framework that provides tensor operations, automatic differentiation, and GPU acceleration."},
    {"id": "d13", "text": "A GPU can accelerate deep learning workloads by performing many matrix and tensor operations in parallel."},
    {"id": "d14", "text": "CUDA is a parallel computing platform and programming model developed by NVIDIA for using NVIDIA GPUs for general-purpose computation."},
    
    {"id": "d15", "text": "Supervised fine-tuning trains a pretrained model on labeled input-output examples so that the model learns a desired behavior or task."},
    {"id": "d16", "text": "Knowledge distillation transfers knowledge from a larger teacher model to a smaller student model using generated or labeled training examples."},
    {"id": "d17", "text": "SFT datasets for tool calling typically contain user requests, available tool definitions, expected tool calls, tool outputs, and final assistant responses."},
    {"id": "d18", "text": "Function calling allows a language model to generate structured information describing which external function should be called and what arguments should be passed to it."},
    
    {"id": "d19", "text": "The Adam optimizer combines momentum-like first-moment estimates with second-moment estimates to adapt the learning rate for individual parameters."},
    {"id": "d20", "text": "Cross-entropy loss is commonly used for classification tasks and language modeling because it measures the difference between predicted probabilities and target probabilities."},
    {"id": "d21", "text": "Overfitting occurs when a machine learning model performs very well on training data but fails to generalize to unseen data."},
    {"id": "d22", "text": "LoRA represents weight updates using low-rank matrices, allowing parameter-efficient fine-tuning of large neural networks."},
    
    {"id": "d23", "text": "The Eiffel Tower is approximately 330 meters tall including its antennas and is one of the most recognizable landmarks in France."},
    {"id": "d24", "text": "The capital city of India is New Delhi, which is located in the National Capital Territory of Delhi."},
    {"id": "d25", "text": "The chemical formula for water is H2O, consisting of two hydrogen atoms bonded to one oxygen atom."},
    {"id": "d26", "text": "Earth completes one rotation around its axis in approximately 24 hours, producing the cycle of day and night."},
    
    {"id": "d27", "text": "A vector database stores numerical vector representations called embeddings and supports similarity-based retrieval."},
    {"id": "d28", "text": "Embeddings represent text, images, or other data as numerical vectors so that semantically similar items can be compared using vector similarity."},
    {"id": "d29", "text": "Cosine similarity measures the similarity between two vectors based on the cosine of the angle between them."},
    {"id": "d30", "text": "Chunking is the process of dividing large documents into smaller pieces before generating embeddings for a RAG pipeline."},
]

def search(query: str, top_k: int = 3):
    query_words = set(query.lower().split())
    scored = []
    for doc in FAKE_DOCS:
        doc_words = set(doc["text"].lower().split())
        overlap = len(query_words & doc_words)
        if overlap > 0:
            scored.append((overlap, doc))
    scored.sort(key=lambda x: -x[0])
    top = [doc["text"] for _, doc in scored[:top_k]]
    if not top:
        return ["No relevant documents found."]
    return top


FAKE_WEATHER = {
    "indore": {"temp_c": 34, "condition": "sunny"},
    "delhi": {"temp_c": 31, "condition": "cloudy"},
    "mumbai": {"temp_c": 29, "condition": "humid"},
    "paris": {"temp_c": 18, "condition": "rainy"},
}

def get_weather(location: str):
    key = location.strip().lower()
    if key not in FAKE_WEATHER:
        raise ValueError(f"No weather data for '{location}'")
    return FAKE_WEATHER[key]


def get_date(operation: str, date1: str = None, date2: str = None):
    if operation == "today":
        return datetime.date.today().isoformat()
    elif operation == "days_between":
        d1 = datetime.date.fromisoformat(date1)
        d2 = datetime.date.fromisoformat(date2)
        return abs((d2 - d1).days)
    else:
        raise ValueError(f"Unknown operation: {operation}")


TOOL_FUNCTIONS = {
    "calculator": calculator,
    "search": search,
    "get_weather": get_weather,
    "get_date": get_date,
}