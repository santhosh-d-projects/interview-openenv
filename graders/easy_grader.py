def grade_easy(answer: str) -> float:
    """
    Grade a candidate's answer to a basic technical question.
    FIX: checks real content keywords from answer_bank, not synthetic prefixes.
    Returns float in [0.0, 1.0].
    """
    answer_lower = answer.lower()
    score = 0.0

    # Strong technical keywords worth rewarding
    strong_keywords = [
        "big o", "o(n)", "o(log n)", "time complexity", "runtime",
        "primary key", "foreign key", "normalization", "normal form",
        "indexing", "pointer", "node", "data structure",
        "binary search", "sorted", "middle element",
        "linked list", "dynamic memory",
    ]

    # Weak/confused signals — reduce score
    weak_signals = ["not sure", "don't remember", "i think", "maybe", "don't know", "somehow"]

    # Partial credit: each keyword match contributes
    for kw in strong_keywords:
        if kw in answer_lower:
            score += 0.15

    # Penalise vague answers
    for ws in weak_signals:
        if ws in answer_lower:
            score -= 0.2

    # Reward sufficiently detailed answers
    if len(answer) > 80:
        score += 0.1
    if len(answer) > 120:
        score += 0.1

    return round(min(max(score, 0.0), 1.0), 2)
