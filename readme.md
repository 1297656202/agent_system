# Multi-Agent Coding System (DeepSeek-R1 Powered)

This project implements a fully automated multi-agent coding system that converts natural language requirements into full software projects. The system uses DeepSeek-R1 as its backend LLM and performs planning, code generation, and evaluation in a structured workflow.

------

## Features

1. Multi-agent architecture
   - PlannerAgent: interprets requirements and generates the project plan
   - CoderAgent: generates code files one by one using DeepSeek-R1
   - EvaluatorAgent: validates file structure and project integrity
2. Robust code generation
   - Generates files individually for stability
   - All file content is Base64 encoded
   - Automatic JSON cleaning
   - Automatic retry when receiving non-JSON output
   - Base64 padding recovery
   - Skips binary files (ico, png, jpg) because LLMs cannot generate them reliably
3. Requirement-driven
   The system reads requirement text from question.txt and builds the full project automatically.

------

## System Workflow

1. The system reads question.txt
2. PlannerAgent analyzes requirements and outputs architecture + tasks
3. CoderAgent generates files in Base64 JSON format
4. Base64 content is decoded and written to real files
5. EvaluatorAgent validates project
6. Final project is saved into workspace/[project_name]

------

## Project Structure

```
agent_system/
├── main.py
├── config.py
├── llm_client.py
├── tasks.py
│
├── agents/
│   ├── base.py
│   ├── planner_agent.py
│   ├── coder_agent.py
│   └── evaluator_agent.py
│
├── tools/
│   ├── file_tools.py
│   └── exec_tools.py
│
├── question.txt
│
└── workspace/   (generated output)
```



------

## Installation

1. Install Python dependencies:
   pip install flask requests feedparser
2. Set DeepSeek API key
   Windows: setx DEEPSEEK_API_KEY "your_api_key_here"
   macOS/Linux: export DEEPSEEK_API_KEY="your_api_key_here"

------

## How to Run

1. Write your requirement into question.txt
2. Execute the system:
   python main.py
3. The generated project will appear in the workspace directory.

------

## Example

Input in question.txt:
 Build an “arXiv CS Daily” web application with category navigation, a daily paper list, and a paper detail page.

The system will automatically generate:

- Flask routes
- HTML templates
- CSS and JavaScript
- arXiv API integration modules
- Citation utilities
- Folder structure and documentation

------

## Known Limitations

- LLMs cannot generate binary files; the system will create empty placeholders.
- Very long responses may still require retry attempts.
- The system generates one file per LLM request for maximum reliability.
