import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        target_path = os.path.join(working_directory, file_path)

        # check that the filepath is NOT outside allowed working directory
        if not os.path.abspath(target_path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        if os.path.getsize(target_path) > MAX_CHARS:
            file_content_string += (
                f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            ) 
        
        return file_content_string
    
    except Exception as e:
        return f'Error reading the file "{file_path}: {e}'