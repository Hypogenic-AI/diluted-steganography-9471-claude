"""
LLM API calling infrastructure with retry logic and cost tracking.
Supports OpenAI and OpenRouter (for Claude, Gemini, etc.).
"""

import os
import time
import json
import httpx
from typing import Optional

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY", "")

# Model configurations
MODELS = {
    "gpt-4.1": {
        "provider": "openai",
        "model_id": "gpt-4.1",
        "display_name": "GPT-4.1",
    },
    "claude-sonnet-4-5": {
        "provider": "openrouter",
        "model_id": "anthropic/claude-sonnet-4-5",
        "display_name": "Claude Sonnet 4.5",
    },
    "gemini-2.5-pro": {
        "provider": "openrouter",
        "model_id": "google/gemini-2.5-pro-preview",
        "display_name": "Gemini 2.5 Pro",
    },
}

# Track costs
_usage_log = []


def call_llm(
    model_key: str,
    prompt: str,
    system: str = "",
    temperature: float = 0.0,
    max_tokens: int = 2048,
    max_retries: int = 5,
) -> dict:
    """
    Call an LLM and return the response text along with usage metadata.

    Returns:
        dict with keys: text, model, input_tokens, output_tokens, latency_s
    """
    model_cfg = MODELS[model_key]
    provider = model_cfg["provider"]
    model_id = model_cfg["model_id"]

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    if provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
    else:  # openrouter
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
        }

    payload = {
        "model": model_id,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    for attempt in range(max_retries):
        try:
            t0 = time.time()
            with httpx.Client(timeout=120.0) as client:
                resp = client.post(url, headers=headers, json=payload)

            latency = time.time() - t0

            if resp.status_code == 429 or resp.status_code >= 500:
                wait = min(2 ** attempt * 2, 60)
                print(f"  [Retry {attempt+1}/{max_retries}] Status {resp.status_code}, waiting {wait}s...")
                time.sleep(wait)
                continue

            resp.raise_for_status()
            data = resp.json()

            text = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})

            result = {
                "text": text,
                "model": model_key,
                "model_id": model_id,
                "input_tokens": usage.get("prompt_tokens", 0),
                "output_tokens": usage.get("completion_tokens", 0),
                "latency_s": round(latency, 2),
            }
            _usage_log.append(result)
            return result

        except Exception as e:
            if attempt < max_retries - 1:
                wait = min(2 ** attempt * 2, 60)
                print(f"  [Retry {attempt+1}/{max_retries}] Error: {e}, waiting {wait}s...")
                time.sleep(wait)
            else:
                return {
                    "text": f"ERROR: {e}",
                    "model": model_key,
                    "model_id": model_id,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "latency_s": 0,
                    "error": str(e),
                }


def get_usage_summary() -> dict:
    """Return cumulative usage statistics."""
    total_input = sum(r["input_tokens"] for r in _usage_log)
    total_output = sum(r["output_tokens"] for r in _usage_log)
    return {
        "total_calls": len(_usage_log),
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "calls_by_model": {
            m: sum(1 for r in _usage_log if r["model"] == m)
            for m in set(r["model"] for r in _usage_log)
        },
    }


if __name__ == "__main__":
    # Quick connectivity test
    print("Testing OpenAI API...")
    result = call_llm("gpt-4.1", "Say 'hello' in one word.", max_tokens=10)
    print(f"  Response: {result['text']}")
    print(f"  Tokens: {result['input_tokens']} in, {result['output_tokens']} out")
    print(f"  Latency: {result['latency_s']}s")

    print("\nTesting OpenRouter (Claude)...")
    result = call_llm("claude-sonnet-4-5", "Say 'hello' in one word.", max_tokens=10)
    print(f"  Response: {result['text']}")
    print(f"  Latency: {result['latency_s']}s")
