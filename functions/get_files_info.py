import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    try:
        if directory == None:
            directory = "."
        directory_path = os.path.join(working_directory, directory)

        # check that the directory is NOT outside allowed working directory
        if not os.path.abspath(directory_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(directory_path):
            return f'Error: "{directory}" is not a directory'
        
        files_info = []
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            files_info.append(
                f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
            )
        
        return "\n".join(files_info)
    
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )