#!/usr/bin/env python3
"""Week-0 smoke test: key, gateway, and tracing, end to end.

    python smoke_test.py            # setup check (run before first class)
    python smoke_test.py --lab [agent_file.py]   # week-1 lab check
"""

import importlib.util
import random
import sys

from course_kit import gateway, trace


def setup_check() -> None:
    print("1) gateway reachable + key valid ...", end=" ")
    with trace.session("week0-smoke") as t:
        reply = gateway.chat(
            [{"role": "user", "content": "Reply with exactly: SMOKE"}],
            headers=t.headers, metadata=t.metadata, max_tokens=5)
        t.finish(task="week0 smoke test", result=reply)
    assert "SMOKE" in reply.upper(), f"unexpected reply: {reply!r}"
    print("ok")
    print("2) trace emitted ... ok (see the course viewer, session 'week0-smoke')")
    print("\nSMOKE TEST PASSED — you are ready for session 1.")


def lab_check(path: str) -> None:
    a, b = random.randint(10**5, 10**6), random.randint(10**5, 10**6)
    task = f"What is {a} * {b}? You must use the calculator."
    spec = importlib.util.spec_from_file_location("student_agent", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    answer = mod.agent(task)
    assert str(a * b) in str(answer).replace(",", ""), \
        f"wrong answer: expected {a*b}, got {answer!r}"
    print(f"LAB CHECK PASSED — {a} * {b} = {a*b}, via your agent.")


if __name__ == "__main__":
    if "--lab" in sys.argv:
        i = sys.argv.index("--lab")
        lab_check(sys.argv[i + 1] if len(sys.argv) > i + 1 else "agent_skeleton.py")
    else:
        setup_check()
