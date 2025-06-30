import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        target_path = os.path.join(working_directory, file_path)
        if not os.path.abspath(target_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        if os.path.split(target_path)[1] == "":
            return f'Error: "{file_path}" is a directory, not a file'
        if not os.path.exists(os.path.dirname(target_path)):
            os.makedirs(os.path.dirname(target_path))

        with open(target_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error creating the file "{file_path}": {e}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to the specified file, constrained to the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory. Overwrites existing file, or creates a new file.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)