# llm_client.py
import os
import json
import requests
from typing import List, Dict, Any, Optional

from config import DEFAULT_LLM_MODEL, LLM_API_BASE, LLM_API_KEY_ENV, USE_REAL_LLM


class LLMClient:
    """
    Thin wrapper around an LLM API.
    When USE_REAL_LLM is False, it falls back to simple mock responses.
    """

    def __init__(self, model: str = DEFAULT_LLM_MODEL):
        self.model = model
        self.use_real_llm = USE_REAL_LLM

        # You can extend this init to support different providers.
        self.api_base = LLM_API_BASE
        self.api_key = os.getenv(LLM_API_KEY_ENV, "")

    def chat(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        """
        Use DeepSeek ChatCompletion API.
        """
        if not self.use_real_llm:
            return self._mock_response(system_prompt, messages)

        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY 环境变量未设置！")

        url = f"{self.api_base}/chat/completions"

        payload = {
            "stream": False,
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                *messages
            ],
            "temperature": 0.5
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=240)
        resp.raise_for_status()

        data = resp.json()
        return data["choices"][0]["message"]["content"]

    # ----------------- mock logic for demo mode -----------------

    # llm_client.py
    def _mock_response(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        """
        Mock response for demo mode, simulating the behavior of PlannerAgent.
        """

        # Check for the planner role in the system_prompt
        if "planner" in system_prompt.lower():
            # Return a mock JSON response representing the architecture and tasks
            return '''{
                "architecture": {
                    "language": "Python",
                    "framework": "Flask",
                    "project_root": "arxiv_cs_daily",
                    "modules": [
                        "app.py",
                        "utils/arxiv_api.py",
                        "templates/index.html",
                        "templates/category.html",
                        "templates/paper.html",
                        "static/styles.css",
                        "requirements.txt",
                        "README.md"
                    ]
                },
                "tasks": [
                    {
                        "id": 1,
                        "name": "Create project skeleton",
                        "description": "Create basic Flask project files.",
                        "files": ["app.py", "requirements.txt", "README.md"],
                        "depends_on": []
                    },
                    {
                        "id": 2,
                        "name": "Implement arxiv_api utilities",
                        "description": "Implement utils/arxiv_api.py to fetch papers from arXiv.",
                        "files": ["utils/arxiv_api.py"],
                        "depends_on": [1]
                    },
                    {
                        "id": 3,
                        "name": "Implement templates",
                        "description": "Implement HTML templates for arXiv categories and paper details.",
                        "files": ["templates/index.html", "templates/category.html", "templates/paper.html", "static/styles.css"],
                        "depends_on": [1]
                    },
                    {
                        "id": 4,
                        "name": "Wire up Flask routes",
                        "description": "Create Flask routes to render templates and handle API calls.",
                        "files": ["app.py"],
                        "depends_on": [1, 2, 3]
                    }
                ]
            }'''
        
        # If not planner, return a generic mock response
        return "Mock LLM response: no specific role detected."


    def _mock_planner(self, user_input: str) -> str:
        """
        Return a static plan for the 'arXiv CS Daily' website as JSON string.
        """
        plan = {
            "architecture": {
                "language": "Python",
                "framework": "Flask",
                "project_root": "arxiv_cs_daily",
                "modules": [
                    "app.py",
                    "utils/arxiv_api.py",
                    "templates/index.html",
                    "templates/category.html",
                    "templates/paper.html",
                    "static/styles.css",
                    "requirements.txt",
                    "README.md",
                ],
            },
            "tasks": [
                {
                    "id": 1,
                    "name": "Create project skeleton",
                    "description": "Create Flask project folders and base files.",
                    "files": ["app.py", "requirements.txt", "README.md"],
                    "depends_on": [],
                },
                {
                    "id": 2,
                    "name": "Implement arxiv_api utilities",
                    "description": "Implement utils/arxiv_api.py to fetch papers by category and id.",
                    "files": ["utils/arxiv_api.py"],
                    "depends_on": [1],
                },
                {
                    "id": 3,
                    "name": "Implement templates",
                    "description": "Implement index.html, category.html, paper.html templates.",
                    "files": [
                        "templates/index.html",
                        "templates/category.html",
                        "templates/paper.html",
                        "static/styles.css",
                    ],
                    "depends_on": [1],
                },
                {
                    "id": 4,
                    "name": "Wire up Flask routes",
                    "description": "Implement Flask routes in app.py using arxiv_api utilities.",
                    "files": ["app.py"],
                    "depends_on": [1, 2, 3],
                },
            ],
        }
        return json.dumps(plan, indent=2)

    def _mock_coder(self, user_input: str) -> str:
        """
        In demo mode, CoderAgent will not directly rely on LLM text,
        so this mock returns a simple message.
        """
        return "Mock coder: please call the built-in code generation helpers."

    def _mock_evaluator(self, user_input: str) -> str:
        """
        Return simple evaluation result.
        """
        return json.dumps({"passed": True, "issues": []})

