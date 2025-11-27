# main.py
from pathlib import Path

from config import PROJECT_ROOT, WORKSPACE_ROOT
from llm_client import LLMClient
from tasks import Plan
from agents.planner_agent import PlannerAgent
from agents.coder_agent import CoderAgent
from agents.evaluator_agent import EvaluatorAgent


def ensure_workspace():
    WORKSPACE_ROOT.mkdir(exist_ok=True)
    print(f"Workspace directory: {WORKSPACE_ROOT}")


def read_requirement(requirement_file: str = "question.txt") -> str:
    """
    Load requirement text from a file.
    Default file: question.txt (placed in PROJECT_ROOT)
    """
    req_path = PROJECT_ROOT / requirement_file

    if not req_path.exists():
        raise FileNotFoundError(
            f"❌ Requirement file not found: {req_path}\n"
            f"Please create a {requirement_file} file under:\n{PROJECT_ROOT}"
        )

    with req_path.open("r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        raise ValueError(
            f"❌ Requirement file '{requirement_file}' is empty.\n"
            "Please write your task description inside."
        )

    print(f"Loaded requirement from file: {req_path}")
    return content


def build():
    """
    End-to-end pipeline for the test case: build project from requirement file.
    """
    ensure_workspace()

    llm = LLMClient()

    planner = PlannerAgent(llm)
    coder = CoderAgent(llm)
    evaluator = EvaluatorAgent(llm)

    # 🔥 Read requirement from file (instead of hardcoding)
    requirement = read_requirement()
    print("\n=== Requirement Loaded ===")
    print(requirement)
    print("==========================\n")

    print("=== [1] Planning phase ===")
    plan: Plan = planner.run(requirement)
    print("Architecture:", plan.architecture)
    print("Tasks:")
    for t in plan.tasks:
        print(f"- ({t.id}) {t.name}: files={t.files}, depends_on={t.depends_on}")

    project_root = plan.architecture.get("project_root", "generated_project")

    print("\n=== [2] Coding phase ===")
    coder.run(plan.tasks, project_root)

    print("\n=== [3] Evaluation phase ===")
    results = evaluator.run(plan.tasks, project_root)
    for r in results:
        print(f"Evaluation result: passed={r.passed}")
        if r.issues:
            print("Issues:")
            for issue in r.issues:
                print(" -", issue)

    print("\n=== Done ===")
    print(f"Generated project under: {WORKSPACE_ROOT / project_root}")
    print("You can now run:")
    print(f"  cd {WORKSPACE_ROOT / project_root}")
    print("  pip install -r requirements.txt")
    print("  python main.py or python app.py (depending on project type)")


if __name__ == "__main__":
    build()
