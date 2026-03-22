# DataSentinel: Autonomous Observability Agent

DataSentinel is an intelligent agentic system built with the **Google Agent Development Kit (ADK)** to automate the diagnostic loop of data pipeline failures.

## 🧠 Core Features

-   **Multi-Agent Orchestration:** A sequential flow between a Lead Orchestrator and specialized sub-agents.
-   **Specialized Sub-Agents:**
    -   `log_analyst`: Expert in parsing pipeline and audit logs.
    -   `data_analyst`: Expert in DuckDB SQL and data integrity metrics.
    -   `code_debugger`: Expert in Python logic and Root Cause Analysis.
-   **Modular Skills:** Uses the ADK "Skills" pattern with metadata-driven instructions and progressive disclosure of business logic.
-   **Safety Guardrails:** Native ADK `before_model` and `before_tool` callbacks to prevent destructive operations and path traversal.

## 🚀 Running the Agent

Ensure you are in the `data-sentinel/` directory.

### 1. CLI Mode
Interact with the agent directly from your terminal.
```bash
uv run adk run datasentinel
```

### 2. Web UI Mode
Launch the local ADK developer interface to visualize agent interactions and tool calls.
```bash
uv run adk web
```

## 📂 Project Structure

-   `datasentinel/agent.py`: Orchestrator and Specialist definitions.
-   `datasentinel/skills/`: Domain-specific instructions (`SKILL.md`) and resources.
-   `datasentinel/tools/`: Diagnostic tools (SQL, Log, and Code readers).
-   `datasentinel/guardrails.py`: Safety logic using ADK callbacks.

## 🛡️ Safety & Ethics
DataSentinel is designed with safety-first principles:
- **Read-Only:** All SQL tools are restricted to SELECT statements.
- **Path Restricted:** Source code access is limited to the target project directory.
- **Sanitized:** PII redaction is applied to findings before they reach the orchestrator.
