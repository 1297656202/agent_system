# tasks.py
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Task:
    id: int
    name: str
    description: str
    files: List[str]
    depends_on: List[int] = field(default_factory=list)


@dataclass
class Plan:
    architecture: Dict[str, Any]
    tasks: List[Task]


@dataclass
class EvaluationResult:
    task_id: int
    passed: bool
    issues: List[str] = field(default_factory=list)

