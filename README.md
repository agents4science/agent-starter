# Agent Starter Kit — AI Agents for Science (Winter 2027)

Your starting point for [CMSC 35370](https://agents4science.github.io/2027/). You will build an AI agent from scratch in the first session and extend it all quarter. This repo gives you the plumbing that is *not* the point of the course — credentials, tracing, the smoke test — so class time goes to the parts that are.

## Week-0 setup (do before the first class)

1. **Install** Python 3.11+ and [Docker Desktop](https://docs.docker.com/desktop/).
2. **Get your gateway key** (sent to you by email; one per student — treat it like a password).
3. Clone this repo, then:

```bash
pip install -r requirements.txt
export AGENTS_GATEWAY_KEY=sk-...        # your personal key
python smoke_test.py
```

You should see `SMOKE TEST PASSED` plus a link to your very first trace. If you don't, post in the course channel *before* the first class — session 1 assumes this works.

## What's in here

| File | What it is |
|---|---|
| `course_kit/trace.py` | **Use this.** One function, `session(name)`, that makes all your agent's model calls appear as a single named, replayable trace. You don't need to understand it in week 1; you will by week 4. |
| `course_kit/gateway.py` | A thin helper for calling the course gateway (any OpenAI-compatible client also works). |
| `agent_skeleton.py` | The week-1 lab, as a skeleton with four marked holes (M1–M4). One on-ramp: fill the holes. |
| `agent_from_scratch.md` | The other on-ramp: the same lab as a spec, no scaffold. Pick whichever matches your background — the deliverable is identical. |
| `smoke_test.py` | Verifies your key, the gateway, and tracing, end to end. |

## The two on-ramps (week 1)

**From scratch** (typically CS students): read `agent_from_scratch.md` and build the loop in an empty file. ~100 lines.

**Skeleton** (typically domain scientists): open `agent_skeleton.py`; the loop structure is given and four holes are marked:
M1 call the model · M2 declare a tool and detect the model's request · M3 execute and feed back · M4 the stop condition.

Either way, by end of session 1 your agent answers a question that *requires* using the calculator tool, and you can watch it do so in your trace.

## Rules of the road

- **Budgets are real.** Your key has a hard spending cap for the quarter. The dashboard shows your balance; running out mid-project is a you-problem we have deliberately made possible. Spend thoughtfully.
- **Traces are captured** for everyone, as course infrastructure — like version control history. (Separately and optionally, you can donate de-identified traces to research; that's a consent form, later, not this repo.)
- **Using AI to write your agent is allowed and expected** — disclose how, and own what you submit.
- Never commit your key. `.gitignore` already covers `.env`.
