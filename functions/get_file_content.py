# We need to  return good error strings for the LLM to understand
import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path= os.path.join(abs_working_directory, file_path)
    if not abs_file_path.startswith(abs_working_directory):
        print(f"abs_working_directory: {abs_working_directory}")
        print(f"abs_file_path: {os.path.join(abs_working_directory, file_path)}")
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) <= MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters].'
                return file_content_string
    except Exception as e:
        print(f"abs_file_path: {abs_file_path}")
        return f'Error reading file "{file_path}": {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)