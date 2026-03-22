from loguru import logger
from config import settings

def read_logs(log_type: str = "pipeline", lines: int = 50) -> str:
    """
    Reads the last few lines of a specific data pipeline log file.
    
    Args:
        log_type: Either 'pipeline' for transformation logs or 'recon' for reconciliation logs.
        lines: The number of lines to read from the end.
        
    Returns:
        The last `lines` lines of the requested log as a single string.
    """
    
    if log_type == "recon":
        log_file = settings.RECON_LOGS_PATH
    else:
        log_file = settings.LOGS_PATH  # Default to pipeline.log

    logger.info(f"Agent reading {log_type} logs (last {lines} lines)...")
    
    if not log_file.exists():
        return f"Log file not found at {log_file}."
        
    try:
        with open(log_file, "r") as f:
            all_lines = f.readlines()
            last_lines = all_lines[-lines:]
            return "".join(last_lines)
    except Exception as e:
        logger.error(f"Log Read Error: {e}")
        return f"Error reading {log_type} logs: {str(e)}"
