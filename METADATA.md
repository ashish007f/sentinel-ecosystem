# Sentinel Ecosystem Metadata

## Project Structure

```text
sentinel-ecosystem/
├── .env                        # Global config (Model API keys, DB paths)
├── docker-compose.yml          # Local orchestration for both projects
│
├── data-pipeline/              # PROJECT 1: The "Target" (Data Engineering)
│   ├── data/                   # Local storage for DuckDB (.db) and CSV mocks
│   ├── logs/                   # Execution logs (Target for the Agent's RCA)
│   ├── src/
│   │   ├── services/           # Mock Kafka / API producers (Faker)
│   │   ├── ingestion/          # Bronze layer loading logic
│   │   └── transformations/    # Silver/Gold SQL logic (DuckDB/SQLAlchemy)
│   ├── scripts/
│   │   ├── run_pipeline.py     # Main E2E pipeline trigger
│   │   └── chaos_monkey.py     # Fault injection (Delete records, nullify data)
│
└── data-sentinel/              # PROJECT 2: The "Agent" (Google ADK)
    ├── datasentinel/           # ADK Agent Directory
    │   ├── agent.py            # RootAgent definition (Tools + Instructions)
    │   └── tools/              # ADK FunctionTools (SQL, LogReader, CodeReader)
    ├── mock_agent_dir/         # Mock Agent for environment verification
    ├── config/
    │   └── adk_config.yaml     # ADK-specific settings
    ├── .env                    # Agent-specific API keys
    ├── pyproject.toml          # Dependency management (uv)
    └── README.md


## Management
- Use `uv` for project management.
- Both `data-pipeline` and `data-sentinel` will have their own workspace managed saperately by uv
