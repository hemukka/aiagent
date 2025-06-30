import os
import subprocess

def run_python_file(working_directory, file_path):
    try:    
        target_path = os.path.join(working_directory, file_path)
        if not os.path.abspath(target_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(target_path):
            return f'Error: File "{file_path}" not found.'
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        complete_process = subprocess.run(
            ["python", file_path],
            cwd=working_directory,
            timeout=30,
            capture_output=True,
            text=True
        )
        output = []
        if complete_process.stdout:
            output.append("STDOUT:\n" + complete_process.stdout)
        if complete_process.stderr:
            output.append("STDERR:\n" + complete_process.stderr)
        if complete_process.returncode != 0:
            output.append(f"Process exited with code {complete_process.returncode}")

        return "\n".join(output) if output else "No output produced."
        
    except Exception as e:
        return f'Error executing Python file "{file_path}": {e}'