# Week 1 lab, from-scratch on-ramp

Build a working tool-calling agent in an empty Python file, ~100 lines, no framework. Same deliverable as the skeleton path.

## Spec

Your program takes a task string and returns an answer, by looping:

1. **Call the model** through the course gateway (`course_kit.gateway.chat`, or any OpenAI-compatible client pointed at the gateway with your key). Maintain a message list; start it with a system prompt that defines a text protocol — the model must reply with exactly one of `THOUGHT:`, `ACTION: calc(<expr>)`, or `FINAL: <answer>`.
2. **Detect tool requests**: if the reply contains an `ACTION:` line, parse out the expression.
3. **Execute and feed back**: evaluate the expression (restrict `eval` — empty `__builtins__`), append the result to the conversation as `OBSERVATION: <result>`, and loop. Errors are observations too — `ERROR: ...` strings go back to the model, which is how it learns to fix its own calls.
4. **Stop** when the reply contains `FINAL:` (return the answer) or after 8 iterations (return a give-up message). Getting this right is the actual lesson of week 1.

## Required plumbing (two lines, not the point of the lab)

Wrap your loop in a trace session so your run is one named, replayable trace:

```python
from course_kit import trace, gateway
with trace.session("week1-yourname") as t:
    reply = gateway.chat(messages, headers=t.headers, metadata=t.metadata)
    ...
    t.finish(task=task, result=answer)
```

## Done when

`python smoke_test.py --lab yourfile.py` passes: your agent correctly answers an arithmetic question it cannot do without the calculator, and the trace shows the tool round-trip.
