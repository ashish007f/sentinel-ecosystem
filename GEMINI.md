## Project Mandates
- **Tooling:** Always use `uv` for dependency management and running scripts.
- **Agent Framework:** Use the **Google ADK** (`google-adk`) for all agentic workflows.
- **Model:** Prefer **`gemini-2.5-flash`** as the default model for all agents.
- **Agent Structure:** Follow the ADK directory pattern: `<agent_dir>/agent.py` containing a `root_agent` variable.
- **Testing Agents:** Use `adk run <agent_dir>` for CLI testing and `adk web` for the Web UI.
- **Python Version:** Use Python 3.12 or higher.

## Architecture & Best Practices
- **Modularity:** Keep components decoupled. Use `src/` for core logic and separate it from scripts or entry points.
- **Interface-Driven Design:** Use Abstract Base Classes (ABCs) or Protocols for external services (e.g., DB storage, LLM providers) to allow easy swapping of implementations.
- **Configuration:** Use environment variables (via `.env`) for all secrets and environment-specific settings. Use a configuration library like `pydantic-settings` to ensure type-safe configuration.
- **Cloud Agnostic:** Avoid hardcoding cloud-specific SDKs in core logic. Wrap them in adapters or use agnostic libraries (e.g., `fsspec` for storage, `litellm` for models).
- **Readability & Type Safety:** Use strict type hints and follow PEP 8. Documentation should focus on the *why* as much as the *how*.
- **Observability:** Implement structured logging throughout the codebase to facilitate RCA (Root Cause Analysis).

## Workspace Context
- `data-pipeline/`: Target data engineering project (DuckDB, SQL, logs).
- `data-sentinel/`: Observability agent project (GenAI, ADK, tools).



