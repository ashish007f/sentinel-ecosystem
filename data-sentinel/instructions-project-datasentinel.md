# Project Objective: DataSentinel RCA Agent
Build an Intelligent Reconciliation Agent that is model-agnostic and cloud-ready.

## Tech Stack
- Framework: Google ADK (Agent Development Kit).
- LLM Proxy: LiteLLM (to support Ollama/Llama3 locally or Gemini on GCP).
- Connection: SQLAlchemy (to query the Pipeline's DuckDB).

## Step-by-Step Implementation
1. **Agent Architecture**:
   - Use `adk create datasentinel` to initialize.
   - Define a `RootAgent` responsible for the investigative loop.

2. **Tool Definition (The "Eyes")**:
   - **ReconTool**: A Python function that runs SQL queries to compare record counts between Bronze/Silver/Gold.
   - **LineageTool**: A hardcoded map (for now) showing that Gold depends on Silver, which depends on Bronze.
   - **LogTool**: A function that reads `pipeline.log` to find Python tracebacks or "Chaos Monkey" events.

3. **Reasoning Logic (The "Brain")**:
   - Prompt Instruction: "When a mismatch is reported, check layers in reverse order (Gold -> Silver -> Bronze). Identify the first point of failure and check logs for that timestamp."

4. **Agnostic Config**:
   - Set up `litellm` in the `.env` file.
   - Default to `ollama/llama3` for local dev; allow override to `vertex_ai/gemini-1.5-pro`.

## Deliverables
- A functional ADK agent that can be queried via CLI: `adk run "Why is Gold revenue low?"`.
- A configuration file for easy cloud migration.
