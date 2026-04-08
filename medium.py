def get_medium_task():
    return {
        "task": "medium",
        "description": "Agent must ask a relevant question targeting the candidate's weak domain.",
        "context": "Candidate is weak in DBMS.",
        "expected_domain": "dbms",
        "example_good_question": "What is normalization and explain its normal forms?",
        "example_bad_question": "Tell me about yourself.",
    }
