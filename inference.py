import os
import sys

# add project root to path so imports work from any directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from env.interview_env import InterviewEnv
from graders.easy_grader import grade_easy
from graders.medium_grader import grade_medium
from graders.hard_grader import grade_hard

MODEL_NAME = os.getenv("MODEL_NAME", "rule-based-agent")
TASK_NAME = os.getenv("TASK_NAME", "interview")
ENV_NAME = "interview_env"
MAX_STEPS = 6


def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action_type, reward, done, error):
    err = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action_type} reward={reward:.2f} done={done_val} error={err}",
        flush=True
    )


def log_end(success, steps, score, rewards):
    success_val = str(success).lower()
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(
        f"[END] success={success_val} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True
    )


def get_action(step: int, state: dict) -> dict:
    """
    Rule-based agent:
      Steps 1-3 → ask questions
      Steps 4-5 → evaluate last answer
      Step 6    → final decision based on accumulated score
    """
    if step <= 3:
        return {"type": "ask", "content": ""}

    if step <= 5:
        score = state.get("score", 0.0)
        answer = state.get("answer", "") or ""
        # simple heuristic: if answer is long and detailed → "good"
        if len(answer) > 100:
            evaluation = "good"
        elif len(answer) > 50:
            evaluation = "average"
        else:
            evaluation = "bad"
        return {"type": "evaluate", "content": evaluation}

    # final decision — base on cumulative score
    score = state.get("score", 0.0)
    decision = "hire" if score >= 1.0 else "reject"
    return {"type": "final_decision", "content": decision}


def run():
    env = InterviewEnv()
    state = env.reset()

    log_start(TASK_NAME, ENV_NAME, MODEL_NAME)

    rewards = []
    success = False
    final_state = state
    steps_done = 0
    questions_asked = 0

    try:
        for step in range(1, MAX_STEPS + 1):
            action = get_action(step, state)

            state, reward, done, info = env.step(action)
            final_state = state
            steps_done = step
            rewards.append(reward)

            if action["type"] == "ask":
                questions_asked += 1

            error = info.get("error")
            log_step(step, action["type"], reward, done, error)

            if done:
                success = state["score"] > 0.5
                break

    except Exception as e:
        log_step(steps_done or 1, "error", 0.0, True, str(e))

    finally:
        total_score = final_state.get("score", 0.0)
        log_end(success, steps_done, total_score, rewards)

        # ----------------------------------------------------------------
        # FIX: actually call graders and report scores
        # ----------------------------------------------------------------
        candidate_type = final_state.get("candidate_type", "average")
        weak_domain = final_state.get("weak_domain", "dbms")
        last_answer = final_state.get("answer") or ""
        last_question = final_state.get("question") or ""
        final_decision = "hire" if total_score >= 1.0 else "reject"

        easy_score = grade_easy(last_answer)
        medium_score = grade_medium(last_question, expected_domain=weak_domain)
        hard_score = grade_hard(
            decision=final_decision,
            candidate_type=candidate_type,
            steps_used=steps_done,
            questions_asked=questions_asked,
        )

        print("", flush=True)
        print("[GRADER_SCORES]", flush=True)
        print(f"  easy_task_score   = {easy_score:.2f}", flush=True)
        print(f"  medium_task_score = {medium_score:.2f}", flush=True)
        print(f"  hard_task_score   = {hard_score:.2f}", flush=True)
        avg = round((easy_score + medium_score + hard_score) / 3, 2)
        print(f"  average_score     = {avg:.2f}", flush=True)

        # print final report if available
        report = getattr(env, "report", {})
        if report:
            print("", flush=True)
            print("[FINAL_REPORT]", flush=True)
            for k, v in report.items():
                print(f"  {k} = {v}", flush=True)


if __name__ == "__main__":
    run()
