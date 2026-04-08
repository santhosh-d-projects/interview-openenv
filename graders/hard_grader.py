def grade_hard(decision: str, candidate_type: str, steps_used: int, questions_asked: int) -> float:
    """
    Grade the full interview outcome.
    Checks: correct hire/reject decision, interview efficiency, question coverage.
    Returns float in [0.0, 1.0].
    """
    decision_lower = decision.lower()
    score = 0.0

    # Decision correctness (most important — 50%)
    if candidate_type == "strong" and "hire" in decision_lower:
        score += 0.5
    elif candidate_type == "weak" and "reject" in decision_lower:
        score += 0.5
    elif candidate_type == "average":
        # either decision is acceptable for average candidate
        if "hire" in decision_lower or "reject" in decision_lower:
            score += 0.35
    else:
        score += 0.1  # made a decision but it was wrong — small participation credit

    # Efficiency bonus — finished in fewer steps (20%)
    if steps_used <= 4:
        score += 0.2
    elif steps_used <= 5:
        score += 0.1

    # Coverage bonus — asked at least 2 questions before deciding (20%)
    if questions_asked >= 3:
        score += 0.2
    elif questions_asked >= 2:
        score += 0.1

    # Participation floor — always give at least 0.1 for completing the episode
    score = max(score, 0.1)

    return round(min(score, 1.0), 2)
