import os
import json
try:
    from groq import Groq
except ImportError:
    Groq = None

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        
        print("DEBUG: Initializing GroqClient (Groq Only Mode)")
        if self.api_key:
            print(f"DEBUG: API Key found (starts with {self.api_key[:5]}...)")
        else:
            print("CRITICAL: No GROQ_API_KEY found in environment variables.")

        if self.api_key and Groq:
            try:
                self.client = Groq(api_key=self.api_key)
                print("DEBUG: Groq client instantiated.")
            except Exception as e:
                print(f"CRITICAL: Failed to initialize Groq client: {e}")
                self.client = None
        else:
            print("CRITICAL: Groq library not installed or API key missing.")
            self.client = None

    def _load_prompt(self, filename):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(base_dir, 'prompts', filename)
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading prompt {filename}: {e}")
            return ""

    def decompose_task(self, task_text):
        """
        Decomposes a task into 3-5 subtasks using Groq.
        """
        if not self.client:
           raise Exception("Groq Client is not initialized. Check API Key.")
        
        try:
            prompt_template = self._load_prompt('decompose.txt')
            if not prompt_template:
                prompt_template = "Break down this task: {{task}} into a JSON list of strings."
            
            system_content = prompt_template.replace("{{task}}", task_text)
            print(f"DEBUG: [Groq] Sending system prompt: {system_content}")

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_content
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            content = chat_completion.choices[0].message.content
            print(f"DEBUG: [Groq] Raw Response: {content}")
            # Cleanup common markdown issues
            content = content.replace("```json", "").replace("```", "").strip()
            # Handle cases where the LLM might return text outside json
            start = content.find('[')
            end = content.rfind(']')
            if start != -1 and end != -1:
                content = content[start:end+1]
            
            return json.loads(content)
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            # No fallback, re-raise or return empty to indicate failure
            raise e

    def phrase_subtask(self, subtask, size):
        """
        Phrases the subtask to be human-friendly based on size (small/medium) using Groq.
        """
        if not self.client:
            raise Exception("Groq Client is not initialized. Check API Key.")
        
        try:
            prompt_template = self._load_prompt('phrase.txt')
            if not prompt_template:
                prompt_template = "Rephrase: {{subtask}} size: {{size}}"

            user_content = prompt_template.replace("{{subtask}}", subtask).replace("{{size}}", size)

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": user_content}
                ],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
             print(f"Error calling Groq API: {e}")
             raise e
