def grade_medium(question: str, expected_domain: str = "dbms") -> float:
    """
    Grade whether the agent asked a question relevant to the candidate's weak domain.
    FIX: checks for domain-specific content keywords, not just the word 'dbms'.
    Returns float in [0.0, 1.0].
    """
    question_lower = question.lower()
    score = 0.0

    domain_keywords = {
        "dbms": [
            "normalization", "primary key", "foreign key", "database",
            "schema", "indexing", "sql", "query", "table", "relation",
            "transaction", "acid", "join", "aggregate",
        ],
        "dsa": [
            "time complexity", "big o", "binary search", "linked list",
            "tree", "graph", "sort", "recursion", "stack", "queue",
            "hash", "dynamic programming", "array",
        ],
        "hr": [
            "yourself", "strength", "weakness", "challenge", "teamwork",
            "leadership", "goal", "pressure", "failure", "achievement",
            "motivation", "career", "conflict",
        ],
    }

    target_keywords = domain_keywords.get(expected_domain, [])

    matched = sum(1 for kw in target_keywords if kw in question_lower)

    if matched >= 2:
        score = 1.0
    elif matched == 1:
        score = 0.6
    else:
        # check if at least another domain's keywords appear (off-topic but not garbage)
        other_keywords = []
        for domain, kws in domain_keywords.items():
            if domain != expected_domain:
                other_keywords.extend(kws)
        if any(kw in question_lower for kw in other_keywords):
            score = 0.2
        else:
            score = 0.1  # completely off-topic but not blank

    return round(score, 2)
