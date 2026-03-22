from loguru import logger
from config import settings

def read_source_code(file_path: str) -> str:
    """
    Reads the content of a source code file within the data-pipeline project.
    
    Args:
        file_path: Relative path from data-pipeline root.
    """
    pipeline_root = settings.PIPELINE_ROOT
    full_path = (pipeline_root / file_path).resolve()
    
    if not full_path.exists():
        return f"Error: File {file_path} not found."

    try:
        with open(full_path, "r") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Code Read Error: {e}")
        return f"Error reading code: {str(e)}"
