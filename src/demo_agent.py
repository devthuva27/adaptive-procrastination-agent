import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from decision_engine import DecisionEngine

def main():
    print("=== Adaptive Procrastination Agent (Terminal Demo) ===")
    
    # Check env var for mock mode, default to True if not set
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("WARNING: No GROQ_API_KEY found. Engine will fail.")

    engine = DecisionEngine()
    
    while True:
        try:
            task = input("\nEnter your task (or 'q' to quit): ")
            if task.lower() == 'q':
                break
            
            task_type = input("Task Type (work/study/chores) [default: general]: ") or "general"
            
            print("\nThinking...")
            suggestion = engine.get_adaptive_subtask(task, task_type)
            
            print(f"\n>>> SUGGESTION ({suggestion['size']}): {suggestion['subtask']}")
            print(f"    (Derived from: {suggestion['original_subtask']})")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
