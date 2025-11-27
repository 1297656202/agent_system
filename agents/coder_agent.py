# agents/coder_agent.py
import json
import re
import base64
from typing import List

from agents.base import BaseAgent
from tasks import Task
from tools.file_tools import create_file
from config import USE_REAL_LLM


CODER_SYSTEM_PROMPT = """
You are CoderAgent.
You MUST output EXACTLY ONE JSON object.
FORMAT:
{
  "path": "relative/path/to/file",
  "content_b64": "base64 encoded file content"
}
Rules:
- Generate ONLY one file per request.
- DO NOT add explanations.
- DO NOT wrap JSON in code fences.
- Base64 must be a single-line string.
"""

class CoderAgent(BaseAgent):
    def __init__(self, llm_client):
        super().__init__("coder", CODER_SYSTEM_PROMPT, llm_client)

    def run(self, tasks: List[Task], project_root: str) -> None:
        if not USE_REAL_LLM:
            raise RuntimeError("Real LLM required for CoderAgent")

        print("=== DeepSeek CoderAgent generating code ===")

        binary_ext = (".ico", ".png", ".jpg", ".jpeg", ".gif", ".pdf")

        for task in tasks:
            print(f"\n[Task {task.id}] {task.name}")
            for file_path in task.files:

                print(f" → Generating file: {file_path}")

                # Skip binary files
                if file_path.lower().endswith(binary_ext):
                    print(f"⚠ Skipping binary file: {file_path}")
                    create_file(f"{project_root}/{file_path}", "")
                    continue

                payload = json.dumps({
                    "project_root": project_root,
                    "file_path": file_path,
                    "task_name": task.name,
                    "task_description": task.description
                }, ensure_ascii=False)

                # retry
                raw = None
                for attempt in range(3):
                    raw = self._chat(payload)
                    clean = self._extract_json(raw)
                    if self._is_json(clean):
                        break
                    print(f"⚠ Non-JSON (attempt {attempt+1}/3). Retrying...")

                if not self._is_json(clean):
                    print("⚠ Attempting JSON repair...")
                    clean = self._repair_json(clean)

                data = json.loads(clean)

                # Strip whitespace from Base64
                content_b64 = data["content_b64"].replace("\n", "").replace(" ", "")

                # Fix padding
                missing = len(content_b64) % 4
                if missing:
                    content_b64 += "=" * (4 - missing)

                # Decode Base64
                content = base64.b64decode(content_b64).decode("utf-8", errors="ignore")

                final_path = f"{project_root}/{data['path']}"
                create_file(final_path, content)

                print("✔ File generated:", final_path)

        print("\n=== CoderAgent completed all tasks ===")

    # ---------------------- Utilities ----------------------

    def _extract_json(self, text: str) -> str:
        """Extract first valid {...} block."""
        t = text.strip()

        # remove fences
        t = t.replace("```json", "").replace("```", "")

        # find first { and last }
        start = t.find("{")
        end = t.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return ""
        return t[start:end+1]

    def _is_json(self, text: str) -> bool:
        if not text.strip().startswith("{"): return False
        try:
            json.loads(text)
            return True
        except:
            return False

    def _repair_json(self, broken: str) -> str:
        """Ask LLM to repair JSON output."""
        repair_prompt = (
            "Fix this JSON. Output JSON only, no commentary:\n"
        )
        fixed = self.llm.chat(repair_prompt, [{"role": "user", "content": broken}])
        return self._extract_json(fixed)
