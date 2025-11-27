# agents/planner_agent.py
import json
import re
from typing import List

from agents.base import BaseAgent
from tasks import Plan, Task


PLANNER_SYSTEM_PROMPT = """
You are a project planning agent.

Your job:
1. Understand the user's requirement.
2. Produce a JSON object with:
   {
     "architecture": {
       "language": "...",
       "framework": "...",
       "project_root": "...",
       "modules": []
     },
     "tasks": [
       {
         "id": 1,
         "name": "...",
         "description": "...",
         "files": [ "main.py", ... ],
         "depends_on": []
       }
     ]
   }
3. IMPORTANT RULES:
   - Output ONLY JSON (no markdown, no explanation)
   - "files" must NOT include project_root prefix
   - Always include at least:
       main.py
       utils.py
       README.md
       requirements.txt
"""

class PlannerAgent(BaseAgent):
    def __init__(self, llm_client):
        super().__init__("planner", PLANNER_SYSTEM_PROMPT, llm_client)

    def run(self, requirement: str) -> Plan:
        print("Requirement received:", requirement)

        raw = self._chat(requirement)
        clean = self._clean_json(raw)

        try:
            data = json.loads(clean)
        except Exception as e:
            print("LLM returned invalid JSON:")
            print(raw)
            raise ValueError(f"JSON decode failed: {e}\nCleaned JSON:\n{clean}")

        architecture = data["architecture"]
        project_root = architecture["project_root"]

        # Fix missing language/framework
        if not architecture.get("language"):
            architecture["language"] = "Python"
        if not architecture.get("framework"):
            architecture["framework"] = "None"

        # Normalize modules
        architecture["modules"] = [
            self._normalize_path(project_root, m)
            for m in architecture.get("modules", [])
        ]

        # Normalize tasks
        tasks: List[Task] = []
        for t in data["tasks"]:
            normalized_files = [
                self._normalize_path(project_root, f)
                for f in t.get("files", [])
            ]
            tasks.append(Task(
                id=int(t["id"]),
                name=t["name"],
                description=t["description"],
                files=normalized_files,
                depends_on=[int(x) for x in t.get("depends_on", [])]
            ))

        # Ensure minimal structure for simple tasks
        self._ensure_minimal_structure(architecture, tasks)

        return Plan(architecture=architecture, tasks=tasks)

    # -------- helper methods --------

    def _clean_json(self, text: str) -> str:
        clean = text.strip()
        clean = re.sub(r"^```(?:json|python)?", "", clean)
        clean = clean.replace("```", "").strip()
        return clean

    def _normalize_path(self, project_root: str, path: str) -> str:
        if path.startswith(project_root + "/"):
            return path[len(project_root) + 1:]
        return path

    def _ensure_minimal_structure(self, architecture, tasks):
        project_root = architecture["project_root"]
        required = ["main.py", "utils.py", "README.md", "requirements.txt"]

        existing = set()
        for t in tasks:
            for f in t.files:
                existing.add(f)

        missing = [f for f in required if f not in existing]
        if not missing:
            return

        max_id = max(t.id for t in tasks)

        for f in missing:
            max_id += 1
            tasks.append(Task(
                id=max_id,
                name=f"Auto-create {f}",
                description=f"System-generated file to ensure minimal structure: {f}",
                files=[f],
                depends_on=[]
            ))
