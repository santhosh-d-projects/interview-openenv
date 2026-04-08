def get_hard_task():
    return {
        "task": "hard",
        "description": "Conduct a full multi-step interview — ask questions, evaluate answers, then make a hire/reject decision.",
        "candidate_type": "strong",
        "expected_decision": "hire",
        "max_steps": 6,
        "scoring": {
            "correct_decision": 0.5,
            "efficiency_bonus": 0.2,
            "coverage_bonus": 0.2,
            "participation_floor": 0.1,
        },
    }
