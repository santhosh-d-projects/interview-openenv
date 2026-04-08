from typing import Dict, List
import random


class InterviewEnv:

    def __init__(self):
        self.max_steps = 6
        self.reset()

    def reset(self) -> Dict:
        self.step_count = 0
        self.done = False
        self.score = 0.0
        self.history = []
        self.last_question = None
        self.last_answer = None
        self.report = {}

        self.candidate_type = random.choice(["strong", "average", "weak"])

        # FIX: wire weak_domain so adaptive questioning actually fires
        self.weak_domain = random.choice(["dsa", "dbms", "hr"])

        self.questions = {
            "dsa": [
                "What is time complexity?",
                "Explain binary search.",
                "What is a linked list?",
            ],
            "dbms": [
                "What is normalization?",
                "What is a primary key?",
                "Explain indexing in databases.",
            ],
            "hr": [
                "Tell me about yourself.",
                "Why should we hire you?",
                "Describe a challenge you overcame.",
            ]
        }

        # FIX: real keyword-rich answers per question per candidate type
        self.answer_bank = {
            "strong": {
                "What is time complexity?":
                    "Time complexity measures how runtime grows with input size using Big O notation like O(n) or O(log n).",
                "Explain binary search.":
                    "Binary search divides a sorted array in half each step, achieving O(log n) by comparing the target to the middle element.",
                "What is a linked list?":
                    "A linked list is a data structure where each node stores data and a pointer to the next node, allowing dynamic memory allocation.",
                "What is normalization?":
                    "Normalization organizes a database to reduce redundancy using normal forms like 1NF, 2NF, and 3NF with primary keys and foreign keys.",
                "What is a primary key?":
                    "A primary key is a unique identifier for each record in a database table, enforcing entity integrity and enabling indexing.",
                "Explain indexing in databases.":
                    "Indexing creates a data structure to speed up query retrieval on a column, trading write overhead for faster read performance.",
                "Tell me about yourself.":
                    "I am a computer science graduate with strong skills in algorithms, databases, and object-oriented programming with internship experience.",
                "Why should we hire you?":
                    "I bring strong technical fundamentals, quick learning ability, and a proven track record of delivering projects on time.",
                "Describe a challenge you overcame.":
                    "I debugged a critical memory leak in a production system under time pressure by systematic profiling and root cause analysis.",
            },
            "average": {
                "What is time complexity?":
                    "Time complexity tells how long an algorithm takes, like O(n) for linear and O(1) for constant time.",
                "Explain binary search.":
                    "Binary search works on sorted arrays by checking the middle element and narrowing the range.",
                "What is a linked list?":
                    "A linked list stores elements using nodes and pointers instead of contiguous memory like arrays.",
                "What is normalization?":
                    "Normalization reduces data repetition in a database by splitting tables based on dependencies.",
                "What is a primary key?":
                    "A primary key uniquely identifies a row in a table and cannot be null.",
                "Explain indexing in databases.":
                    "Indexing helps queries run faster by creating a lookup structure on a column.",
                "Tell me about yourself.":
                    "I am a fresher with knowledge of programming languages and some project experience.",
                "Why should we hire you?":
                    "I am a hard worker and a quick learner who adapts well to new environments.",
                "Describe a challenge you overcame.":
                    "I had trouble with a group project deadline but we managed to complete it by dividing tasks.",
            },
            "weak": {
                "What is time complexity?":
                    "It is about the time taken by a program. Not sure about the exact definition.",
                "Explain binary search.":
                    "Binary search is a search method. I think it searches from both ends.",
                "What is a linked list?":
                    "It is a list of linked items. I don't remember the exact structure.",
                "What is normalization?":
                    "Normalization makes data normal or standard. I am not very clear on this.",
                "What is a primary key?":
                    "A key used in databases. I think it identifies something.",
                "Explain indexing in databases.":
                    "Indexing is like numbering things. It helps find data maybe.",
                "Tell me about yourself.":
                    "I am a student. I have studied some subjects and looking for a job.",
                "Why should we hire you?":
                    "I will work hard and learn things.",
                "Describe a challenge you overcame.":
                    "I had some difficulties in college but managed somehow.",
            }
        }

        return self.state()

    def state(self) -> Dict:
        return {
            "question": self.last_question,
            "answer": self.last_answer,
            "history": self.history,
            "score": round(self.score, 2),
            "steps_left": self.max_steps - self.step_count,
            "candidate_type": self.candidate_type,
            "weak_domain": self.weak_domain,
        }

    def step(self, action: Dict):
        if self.done:
            return self.state(), 0.0, True, {"error": "episode finished"}

        self.step_count += 1
        reward = 0.0
        error = None

        action_type = action.get("type")
        content = action.get("content", "")

        # -------- ASK --------
        if action_type == "ask":
            # FIX: adaptive domain selection using weak_domain
            domain = self.weak_domain if self.weak_domain else random.choice(list(self.questions.keys()))
            question = random.choice(self.questions[domain])

            # FIX: check BEFORE appending so repetition logic is correct
            if question in self.history:
                reward -= 0.3
                error = "repeated question"
            else:
                reward += 0.3

            self.last_question = question
            self.last_answer = self._simulate_answer(question)
            self.history.append(question)

        # -------- EVALUATE --------
        elif action_type == "evaluate":
            # FIX: block scoring entirely if no answer exists yet
            if not self.last_answer:
                return self.state(), 0.0, False, {"error": "no answer to evaluate yet"}

            quality = self._evaluate_answer(self.last_answer)

            if quality == "good" and "good" in content.lower():
                reward += 0.4
            elif quality == "average" and "average" in content.lower():
                reward += 0.3
            elif quality == "bad" and ("bad" in content.lower() or "poor" in content.lower()):
                reward += 0.3
            else:
                reward += 0.1  # partial credit for attempting evaluation

            # flow reward: reward multi-step reasoning
            if len(self.history) >= 2:
                reward += 0.1

        # -------- FINAL DECISION --------
        elif action_type == "final_decision":
            if self.candidate_type == "strong" and "hire" in content.lower():
                reward += 1.0
            elif self.candidate_type == "weak" and "reject" in content.lower():
                reward += 1.0
            elif self.candidate_type == "average":
                # average candidate — either is defensible, give partial
                reward += 0.5
            else:
                reward += 0.2

            self.report = {
                "candidate_type": self.candidate_type,
                "weak_domain": self.weak_domain,
                "questions_asked": len(self.history),
                "final_decision": content,
                "total_score": round(self.score + reward, 2),
            }

            self.done = True

        else:
            reward -= 0.5
            error = "invalid action type"

        self.score += reward

        if self.step_count >= self.max_steps:
            self.done = True

        return self.state(), round(reward, 2), self.done, {"error": error}

    def _simulate_answer(self, question: str) -> str:
        # FIX: pull from answer bank, fall back gracefully
        bank = self.answer_bank.get(self.candidate_type, {})
        return bank.get(question, f"I am not sure about {question}.")

    def _evaluate_answer(self, answer: str) -> str:
        answer_lower = answer.lower()
        # quality indicators based on real answer content
        strong_signals = [
            "o(", "log n", "big o", "primary key", "foreign key",
            "normalization", "normal form", "indexing", "pointer",
            "data structure", "profiling", "root cause", "entity integrity"
        ]
        weak_signals = [
            "not sure", "don't remember", "not very clear",
            "i think", "maybe", "somehow", "don't know"
        ]

        strong_count = sum(1 for s in strong_signals if s in answer_lower)
        weak_count = sum(1 for w in weak_signals if w in answer_lower)

        if strong_count >= 2 or len(answer) > 100:
            return "good"
        elif weak_count >= 2 or len(answer) < 50:
            return "bad"
        else:
            return "average"
