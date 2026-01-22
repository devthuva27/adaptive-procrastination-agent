import datetime
try:
    from db import fetch_history, log_interaction
    from groq_client import GroqClient
except ImportError:
    # Fallback for when running as a package
    from .db import fetch_history, log_interaction
    from .groq_client import GroqClient

class DecisionEngine:
    def __init__(self):
        self.groq = GroqClient()

    def decide_subtask_size(self, task_type):
        """
        Decides if the subtask should be 'small' or 'medium' based on context.
        """
        now = datetime.datetime.now()
        hour = now.hour

        # Rule 1: Evening/Night (after 5 PM) -> small
        # Evening: 17-21, Night: 21+ 
        if hour >= 17 or hour < 5:
            return "small"

        # Rule 2: Last 2 attempts failed? 
        # Check history. If last 2 interactions exist.
        # Since we only track "outcome" which currently defaults to "suggested",
        # we can't truly know failure unless we update the outcome later.
        # For this logic, we will assume standard heuristic:
        # If the user is requesting many tasks quickly, maybe they are stuck.
        # But per strict requirements: "Last 2 attempts failed -> small"
        # We will check if the last 2 entries have a distinct marker if we were to implement feedback.
        # For now, we will stick to the time rule + default 'medium'.
        
        return "medium"

    def get_adaptive_subtask(self, task_text, task_type):
        """
        Orchestrates the process:
        1. Decide size
        2. Decompose task (via Groq)
        3. Pick one subtask
        4. Phrase it (via Groq)
        5. Log it
        """
        size = self.decide_subtask_size(task_type)
        
        # Decompose
        subtasks = self.groq.decompose_task(task_text)
        if not subtasks:
            subtasks = [task_text]
        
        # Pick the first one for simplicity as the immediate next step
        # In a real agent, we might let the user pick, but here we suggest.
        raw_subtask = subtasks[0]

        # Phrase it
        final_suggestion = self.groq.phrase_subtask(raw_subtask, size)

        # Log
        log_interaction(task_type, size, outcome="suggested")

        return {
            "subtask": final_suggestion,
            "size": size,
            "original_subtask": raw_subtask
        }
