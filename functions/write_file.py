import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        parent_dir = os.path.dirname(abs_file_path)
        try:
            if not os.path.isdir(parent_dir):
                os.makedirs(parent_dir)
        except Exception as e:
            return f'Error: Cannot create parent directories for "{parent_dir}": {e}'
        # return f'Error: Path "{file_path}" is not a regular file'
    dir_name = os.path.dirname(abs_file_path)
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(abs_file_path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Cannot write to file "{file_path}": {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites an existing file or writes to a new file if it does not exist, creating parent directories if necessary, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file as a string",
            )
        },
    ),
)