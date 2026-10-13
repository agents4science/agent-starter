"""Minimal helper for the course gateway. Any OpenAI-compatible client works
too; this exists so week 1 needs zero client-library knowledge."""

import os

import requests

GATEWAY = os.environ.get("AGENTS_GATEWAY_URL", "http://localhost:4000")
KEY = os.environ.get("AGENTS_GATEWAY_KEY", "")
DEFAULT_MODEL = os.environ.get("AGENTS_MODEL", "argonne-coder")


def chat(messages, model=DEFAULT_MODEL, headers=None, metadata=None, **kwargs):
    """One chat completion via the course gateway. Returns the reply text.

    Pass ``headers=t.headers`` and ``metadata=t.metadata`` from a
    course_kit.trace session so the call lands in your named trace.
    """
    if not KEY:
        raise RuntimeError("set AGENTS_GATEWAY_KEY to your personal key")
    body = {"model": model, "messages": messages, **kwargs}
    if metadata:
        body["metadata"] = metadata
        body["user"] = metadata.get("student", "")
    r = requests.post(f"{GATEWAY}/v1/chat/completions",
                      headers={"Authorization": f"Bearer {KEY}", **(headers or {})},
                      json=body, timeout=120)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
