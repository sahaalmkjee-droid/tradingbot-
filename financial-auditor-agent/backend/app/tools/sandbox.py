import sys
import subprocess
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def execute_python_code(code: str, timeout: int = 5) -> Dict[str, Any]:
    """
    Execute Python code string in an isolated subprocess with a strict timeout.
    Returns standard output, error output, and execution result status.
    """
    try:
        # Wrap execution in isolated subprocess
        process = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        stdout = process.stdout.strip()
        stderr = process.stderr.strip()
        success = (process.returncode == 0)
        
        parsed_result = None
        if success and stdout:
            # Try parsing json if stdout contains json
            try:
                # Find last JSON object string if standard print output has commentary
                lines = stdout.splitlines()
                for line in reversed(lines):
                    if line.startswith("{") and line.endswith("}"):
                        parsed_result = json.loads(line)
                        break
                if parsed_result is None and stdout.startswith("{"):
                    parsed_result = json.loads(stdout)
            except Exception:
                pass
                
        return {
            "success": success,
            "returncode": process.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "parsed_result": parsed_result
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": f"Execution timed out after {timeout} seconds.",
            "parsed_result": None
        }
    except Exception as e:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "parsed_result": None
        }
