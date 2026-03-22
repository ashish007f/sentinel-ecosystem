from google.adk.agents.llm_agent import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.skills import load_skill_from_dir
from google.adk.tools.skill_toolset import SkillToolset
from datasentinel.tools.db_tool import query_db
from datasentinel.tools.log_tool import read_logs
from datasentinel.tools.code_tool import read_source_code
from config import settings
from datasentinel.guardrails import sanitize_user_input, sanitize_tool_calls
from pathlib import Path

# --- Helper: Load Skill ---
def get_skill_toolset(skill_name: str) -> SkillToolset:
    skill_path = Path(__file__).parent / "skills" / skill_name
    skill = load_skill_from_dir(skill_path)
    return SkillToolset(skills=[skill])

# --- Specialist Definition ---

# Log Analyst with Skill
log_analyst = Agent(
    model=LiteLlm(model=settings.MODEL_NAME),
    name='log_analyst',
    description="Specialist in analyzing pipeline and reconciliation logs.",
    instruction="Focus on the logs to find discrepancies. Use your skill tools.",
    tools=[read_logs, get_skill_toolset("log-analyst-skill")],
    before_model_callback=sanitize_user_input,
    before_tool_callback=sanitize_tool_calls,
)

# Data Analyst with Skill
data_analyst = Agent(
    model=LiteLlm(model=settings.MODEL_NAME),
    name='data_analyst',
    description="Specialist in querying the DuckDB warehouse for data integrity.",
    instruction="Verify counts in DuckDB. Use your skill tools for consistent analysis.",
    tools=[query_db, get_skill_toolset("data-analyst-skill")],
    before_model_callback=sanitize_user_input,
    before_tool_callback=sanitize_tool_calls,
)

# Code Debugger with Skill
code_debugger = Agent(
    model=LiteLlm(model=settings.MODEL_NAME),
    name='code_debugger',
    description="Specialist in inspecting Python source code for logic bugs.",
    instruction="Find bugs in the pipeline logic. Use your skill tools for deep inspection.",
    tools=[read_source_code, get_skill_toolset("code-debugger-skill")],
    before_model_callback=sanitize_user_input,
    before_tool_callback=sanitize_tool_calls,
)

# --- Orchestrator: Root Agent ---
root_agent = SequentialAgent(
    name='datasentinel_orchestrator',
    description="Sentinel Ecosystem root cause analysis Orchestrator (Sequential mode)",
    sub_agents=[log_analyst, data_analyst, code_debugger]
)
