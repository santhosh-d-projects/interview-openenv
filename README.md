# Placement Interview Trainer Environment

An OpenEnv-compatible simulation where an AI agent conducts placement interviews — asking technical questions, evaluating candidate responses, and making hire/reject decisions.

## What it does

The agent operates inside a step-based environment that simulates a candidate (strong / average / weak). Each episode the agent must:

1. Ask relevant questions targeting the candidate's weak domain
2. Evaluate answers correctly
3. Make a final hire or reject decision

The environment adapts: a strong candidate gives detailed, keyword-rich answers; a weak candidate gives vague, short responses.

## Features

- Candidate personality simulation (strong / average / weak)
- Adaptive questioning based on candidate's weak domain (DSA / DBMS / HR)
- Real answer bank with domain-specific content per candidate type
- Multi-step reward shaping — partial credit at every step
- Repetition penalty — agent is penalised for asking the same question twice
- Final report generated at end of episode
- Three graded tasks with deterministic scoring

## Actions

| Action type | Content | Effect |
|---|---|---|
| `ask` | `""` | Ask next question from weak domain |
| `evaluate` | `"good"` / `"average"` / `"bad"` | Evaluate last candidate answer |
| `final_decision` | `"hire"` / `"reject"` | End episode with decision |

## Observations

```json
{
  "question": "last question asked",
  "answer": "candidate's response",
  "history": ["list of asked questions"],
  "score": 1.2,
  "steps_left": 2,
  "candidate_type": "strong",
  "weak_domain": "dbms"
}
```

## Reward structure

| Behaviour | Reward |
|---|---|
| New relevant question | +0.3 |
| Repeated question | -0.3 |
| Correct evaluation | +0.3 to +0.4 |
| Multi-step flow bonus | +0.1 |
| Correct final decision | +0.5 to +1.0 |

## Tasks

**Easy** — Given a candidate answer, the grader checks if it contains correct technical keywords. Partial credit per keyword matched.

**Medium** — Agent must ask a question relevant to the candidate's weak domain. Grader checks for domain-specific content keywords in the question.

**Hard** — Full interview episode. Grader scores: decision correctness (50%) + efficiency (20%) + question coverage (20%) + participation floor (10%).

## How to run

```bash
python inference.py
```

Expected output:

```
[START] task=interview env=interview_env model=rule-based-agent
[STEP] step=1 action=ask reward=0.30 done=false error=null
...
[END] success=true steps=6 score=1.00 rewards=...

[GRADER_SCORES]
  easy_task_score   = 0.55
  medium_task_score = 0.60
  hard_task_score   = 0.55
  average_score     = 0.57

[FINAL_REPORT]
  candidate_type = average
  weak_domain = dsa
  ...
```

## Docker

```bash
docker build -t interview-env .
docker run interview-env
```

## Project structure

```
project/
├── env/
│   └── interview_env.py
├── tasks/
│   ├── easy.py
│   ├── medium.py
│   └── hard.py
├── graders/
│   ├── easy_grader.py
│   ├── medium_grader.py
│   └── hard_grader.py
├── inference.py
├── openenv.yaml
├── Dockerfile
├── requirements.txt
└── README.md
```
