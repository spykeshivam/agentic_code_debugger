import os
import subprocess
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        final_args=["python", abs_file_path] + args
        output = subprocess.run(final_args, timeout=30, capture_output=True, cwd=abs_working_directory, text=True)
        final_string = f"""
STDOUT:{output.stdout}
STDERR:{output.stderr}
"""
        if output.stderr=="" and output.stdout=="":
            final_string = "No output from the script."
        if output.returncode != 0:
            final_string = f"Error: Python script exited with code {output.returncode}\n{final_string}"
        return final_string
    except Exception as e:
        f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file with python3 interpreter. Accepts additional CLI args as an optional array.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of strings to pass as command line arguments to the Python script.",
                items=types.Schema(type=types.Type.STRING),
            )
        },
    ),
)