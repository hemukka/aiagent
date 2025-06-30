import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:    
        target_path = os.path.join(working_directory, file_path)
        if not os.path.abspath(target_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(target_path):
            return f'Error: File "{file_path}" not found.'
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        commands = ["python", file_path]
        if args:
            commands.extend(args)
        complete_process = subprocess.run(
            commands,
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
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the specified Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional arguments for the Python file to be executed.",
            ),
        },
    ),
)