#!/usr/bin/env python3
"""Week 1 lab, skeleton on-ramp: a bare agent loop with four holes to fill.

Milestones (fill them in order; each is independently testable):
  M1  call the model
  M2  declare a tool and detect when the model asks for it
  M3  execute the tool and feed the result back
  M4  the stop condition

Run:  python agent_skeleton.py "What is 123456 multiplied by 654321?"
Done when: the agent answers using the calculator (check your trace!), and
`python smoke_test.py --lab` passes.
"""

import re
import sys

from course_kit import gateway, trace

SYSTEM = """You solve tasks step by step. You have one tool:
  calc(expression) - evaluate a Python arithmetic expression
Respond with EXACTLY one of:
  THOUGHT: <reasoning>
  ACTION: calc(<expression>)
  FINAL: <answer>
After an ACTION you will receive an OBSERVATION. Begin."""

MAX_ITERS = 8


def run_tool(action_text: str) -> str:
    """M3 (part 1): parse 'calc(<expr>)' and evaluate the expression.

    Hints: a regex like  calc\\((.*)\\)  gets the argument; evaluate with
    eval(expr, {"__builtins__": {}}, {}) so nothing dangerous is reachable.
    Return the result as a string, or an 'ERROR: ...' string on failure.
    """
    # TODO(M3) ------------------------------------------------------------
    raise NotImplementedError("M3: implement run_tool")
    # ---------------------------------------------------------------------


def agent(task: str) -> str:
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"TASK: {task}"}]

    with trace.session(f"week1-{gateway.KEY[-6:]}") as t:
        for i in range(MAX_ITERS):
            # M1: call the model through the course gateway.
            # Hint: gateway.chat(messages, headers=t.headers, metadata=t.metadata)
            # TODO(M1) -----------------------------------------------------
            reply = ...
            # --------------------------------------------------------------
            messages.append({"role": "assistant", "content": reply})

            # M4: if the model gave a FINAL answer, stop and return it.
            # Hint: re.search(r"FINAL:\s*(.+)", reply, re.S)
            # TODO(M4) -----------------------------------------------------

            # --------------------------------------------------------------

            # M2: detect an ACTION line; if present, extract it.
            # Hint: re.search(r"ACTION:\s*(.+)", reply)
            # TODO(M2) -----------------------------------------------------
            action = ...
            # --------------------------------------------------------------

            # M3 (part 2): run the tool and feed the OBSERVATION back.
            obs = run_tool(action) if action else \
                "ERROR: reply had no ACTION or FINAL; use the required format"
            messages.append({"role": "user", "content": f"OBSERVATION: {obs}"})

        result = f"gave up after {MAX_ITERS} iterations"
        t.finish(task=task, result=result)
        return result


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "What is 123456 * 654321?"
    print(agent(task))
