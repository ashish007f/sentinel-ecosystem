from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from typing import Any, Dict, Optional
from loguru import logger
from google.genai import types # For creating response content

def sanitize_user_input(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    """
    Inspects the latest user message for 'BLOCK'. If found, blocks the LLM call
    and returns a predefined LlmResponse. Otherwise, returns None to proceed.
    """
    logger.info(f"[Safety] RootAgent pre-check for model: {llm_request.model} & agent: {callback_context.agent_name}")

    for content in reversed(llm_request.contents):
        if content.role == 'user' and content.parts:
            for part in content.parts:
                if part.text:
                    if "password" in part.text.lower():
                        logger.warning("Safety Violation: 'PASSWORD' detected in user input. Blocking LLM call.")
                        return LlmResponse(
                            content=types.Content(
                            role="model", # Mimic a response from the agent's perspective
                            parts=[types.Part(text="I cannot process this request because it contains the blocked keyword 'PASSWORD'.")])
                        )

    return None  # No issues found, proceed with the LLM call

def sanitize_tool_calls(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[dict]:
    """
    Standard ADK Hook: Called before a tool is executed.
    Expected signature: (tool: BaseTool, args: dict[str, Any], context: ToolContext)
    """
    tool_name = tool.name
    logger.info(f"[Safety] Validating tool call: {tool_name}")

    # 1. SQL Injection / Destructive Query Protection
    if tool_name == "query_duckdb":
        query = args.get("query", "").upper()
        if not query.strip().startswith("SELECT"):
            logger.error(f"Safety Violation: Non-SELECT query detected in {tool_name}")
            tool_context.state["guardrail_tool_block_triggered"] = True
            return {
                "status": "error",
                "error_message": f"Safety Error: Tool '{tool_name}' only supports SELECT queries."
            }
        destructive_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE", "ALTER"]
        if any(f" {kw} " in f" {query} " for kw in destructive_keywords):
            logger.error(f"Safety Violation: Destructive keyword detected in {tool_name}")
            tool_context.state["guardrail_tool_block_triggered"] = True
            return {
                "status": "error",
                "error_message": f"Safety Error: Destructive SQL keywords are forbidden in '{tool_name}'."
            }

    # 2. Path Traversal & Unauthorized Access Protection
    if tool_name == "read_source_code":
        file_path = args.get("file_path", "")
        if ".." in file_path or file_path.startswith("/") or ":" in file_path:
            logger.error(f"Safety Violation: Path traversal in {tool_name}")
            tool_context.state["guardrail_tool_block_triggered"] = True
            return {
                "status": "error",
                "error_message": f"Safety Error: Path traversal is forbidden in '{tool_name}'."
            }
        
        allowed_prefixes = ["src/", "logs/", "scripts/"]
        if not any(file_path.startswith(prefix) for prefix in allowed_prefixes):
            logger.error(f"Safety Violation: Unauthorized directory access in {tool_name}")
            tool_context.state["guardrail_tool_block_triggered"] = True
            return {
                "status": "error",
                "error_message": f"Safety Error: Access to '{file_path}' is outside permitted directories."
            }
        
    # 3. read logs tool: limit log types and lines
    if tool_name == "read_pipeline_logs":
        log_type = args.get("log_type")
        if log_type not in ["pipeline", "recon"]:
            logger.error(f"Safety Violation: Invalid log type in {tool_name}")
            tool_context.state["guardrail_tool_block_triggered"] = True
            return {
                "status": "error",
                "error_message": f"Safety Error: Invalid log type '{log_type}' in '{tool_name}'."
            }
        
    # If no guardrails are triggered, return None to proceed with the tool call
    return None
