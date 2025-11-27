# config.py
from pathlib import Path

# Root directory of this project
PROJECT_ROOT = Path(__file__).parent

# Workspace where the generated code project will be created
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"

# Whether to use a real LLM API.
# If False, agents will use built-in demo logic so you can run without API keys.
USE_REAL_LLM = True

# Default LLM model configuration (placeholder)
DEFAULT_LLM_MODEL = "deepseek-chat"
LLM_API_BASE = "https://api.deepseek.com"    # DeepSeek 官方 API 地址
LLM_API_KEY_ENV = "DEEPSEEK_API_KEY"         # 让 Key 放环境变量

# Misc settings
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

