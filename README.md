# Sentinel Ecosystem: Agentic Data Observability

Sentinel is a modular ecosystem demonstrating the power of **Autonomous AI Agents** in Data Engineering. It consists of a robust data pipeline and an intelligent observability agent that detects, diagnoses, and proposes fixes for pipeline failures.

## 🚀 Project Overview

The ecosystem is split into two primary components:

1.  **[data-pipeline/](./data-pipeline/):** A DuckDB-powered ELT pipeline that processes synthetic user data through Bronze (Raw), Silver (Cleaned), and Gold (Aggregated) layers. It includes a "Chaos Monkey" for fault injection and a Reconciliation job for integrity auditing.
2.  **[data-sentinel/](./data-sentinel/):** An advanced Observability Agent built with the **Google Agent Development Kit (ADK)**. It uses multi-agent orchestration (Log Analyst, Data Analyst, Code Debugger) to perform automated Root Cause Analysis (RCA).

## 🛠️ Tech Stack

-   **Framework:** [Google ADK](https://google.github.io/adk-docs/)
-   **Database:** DuckDB (In-process OLAP)
-   **Project Management:** `uv`
-   **LLM Integration:** Gemini 2.5 Flash / LiteLLM
-   **Core Libraries:** Pandas, Pydantic-Settings, Loguru

## ⚙️ Setup & Installation

### 1. Prerequisites
- Install [uv](https://github.com/astral-sh/uv) (The lightning-fast Python package manager).
- Obtain a **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).

### 2. Configure Environment
Create a `.env` file in `data-sentinel/` folders:
```env
GEMINI_API_KEY=your_api_key_here
MODEL_NAME=gemini/gemini-2.5-flash
```

### 3. Run the Data Pipeline
```bash
cd data-pipeline
uv run scripts/run_pipeline.py  # Run E2E pipeline
uv run scripts/run_recon.py     # Run integrity audit
uv run scripts/chaos_monkey.py  # Inject failures (Optional)
```

### 4. Run the Sentinel Agent (RCA)
```bash
cd data-sentinel
# CLI Mode
uv run adk run datasentinel

# Web UI Mode
uv run adk web
```

## 🧠 How it Works: The RCA Loop
When a failure occurs (e.g., records are missing in the Silver layer):
1.  **Log Analyst:** Scans `recon.log` to identify the layer mismatch.
2.  **Data Analyst:** Queries DuckDB to verify row counts and NULL distributions.
3.  **Code Debugger:** Reads the `data-pipeline` source code to find logic bugs.
4.  **Orchestrator:** Synthesizes findings into a final report with a specific code fix.

---
Built with ❤️ using Google ADK and DuckDB.
