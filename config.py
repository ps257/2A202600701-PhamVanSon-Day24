"""Shared configuration for Lab 24: Eval + Guardrail Stack."""

import os
import sys
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

# --- API Keys ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")  # Optional: for HuggingFace models

# --- Qdrant (same as Day 18) ---
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "lab24_production"

# --- Embedding (same as Day 18) ---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# --- Chunking (same as Day 18) ---
HIERARCHICAL_PARENT_SIZE = 2048
HIERARCHICAL_CHILD_SIZE = 256
SEMANTIC_THRESHOLD = 0.85

# --- Search (same as Day 18) ---
BM25_TOP_K = 20
DENSE_TOP_K = 20
HYBRID_TOP_K = 20
RERANK_TOP_K = 3

# --- Paths ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEST_SET_PATH = os.path.join(os.path.dirname(__file__), "test_set_50q.json")
ANSWERS_PATH = os.path.join(os.path.dirname(__file__), "answers_50q.json")
HUMAN_LABELS_PATH = os.path.join(os.path.dirname(__file__), "human_labels_10q.json")
ADVERSARIAL_SET_PATH = os.path.join(os.path.dirname(__file__), "adversarial_set_20.json")
GUARDRAILS_CONFIG_DIR = os.path.join(os.path.dirname(__file__), "guardrails")

# --- LLM Judge ---
JUDGE_MODEL = os.getenv("MODEL_API_KEY", "openrouter/free") if os.getenv("OPENAI_API_KEY", "").startswith("sk-or-") else "gpt-4o-mini"

# --- Guardrail latency budget ---
LATENCY_BUDGET_P95_MS = 500  # target: full guard stack P95 < 500ms
PRESIDIO_LANGUAGE = "en"    # Presidio base language; custom VN recognizers added via PatternRecognizer


def get_llm_client():
    """Return OpenAI client and model name, supporting both OpenAI and OpenRouter."""
    from openai import OpenAI
    key = os.getenv("OPENAI_API_KEY", "")
    base_url = os.getenv("OPENAI_BASE_URL", os.getenv("OPENAI_API_BASE", None))
    
    if key.startswith("sk-or-"):
        model = os.getenv("MODEL_API_KEY", "openai/gpt-4o-mini")
        return OpenAI(api_key=key, base_url=base_url or "https://openrouter.ai/api/v1"), model
    else:
        return OpenAI(api_key=key, base_url=base_url), "gpt-4o-mini"
