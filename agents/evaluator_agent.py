# agents/evaluator_agent.py
import json
from pathlib import Path
from typing import List

from llm_client import LLMClient
from agents.base import BaseAgent
from tasks import Task, EvaluationResult
from tools.exec_tools import run_command
from tools.file_tools import ensure_workspace_subpath


EVALUATOR_SYSTEM_PROMPT = """
You are a code evaluation agent.
You will receive metadata about generated files and test outputs.
Your job is to summarize whether the task passed and list issues.
Return JSON: {"passed": bool, "issues": [string, ...]}
"""


class EvaluatorAgent(BaseAgent):
    def __init__(self, llm_client: LLMClient):
        super().__init__("evaluator", EVALUATOR_SYSTEM_PROMPT, llm_client)

    def run(self, tasks: List[Task], project_root: str) -> List[EvaluationResult]:
        """
        Evaluate the generated project.
        Currently we do lightweight checks:
        - Ensure expected files exist.
        - Try to compile Python files.
        """
        results: List[EvaluationResult] = []

        root_path = ensure_workspace_subpath(project_root)

        # File existence check
        missing_files = []
        for t in tasks:
            for f in t.files:
                target = root_path / f
                if not target.exists():
                    missing_files.append(str(target))

        issues = []
        if missing_files:
            issues.append(f"Missing files: {missing_files}")

        # Try compileall
        code, out, err = run_command(["python", "-m", "compileall", project_root])
        if code != 0:
            issues.append(f"Python compileall failed: {err}")

        # You could also call LLM here with logs & issues for richer analysis.
        # For now we simply aggregate into one EvaluationResult.
        passed = len(issues) == 0
        results.append(EvaluationResult(task_id=-1, passed=passed, issues=issues))

        return results

