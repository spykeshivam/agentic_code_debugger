import os
from google.genai import types


def get_files_info(working_directory, directory="None"):
    abs_working_directory = os.path.abspath(working_directory)
    if directory == "None":
        directory = abs_working_directory
        abs_directory= os.path.abspath(directory)
    abs_directory= os.path.abspath(os.path.join(working_directory, directory))
    print(f"abs_working_directory: {abs_working_directory}")
    print(f"abs_directory: {abs_directory}")
    if not abs_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'
    
    contents = os.listdir(abs_directory)
    final_response = f"Results for {abs_directory} directory:\n"
    for content in contents:
        is_dir = os.path.isdir(os.path.join(abs_directory, content))
        file_info = os.path.getsize(os.path.join(abs_directory, content))
        final_response += f"{content}: file_size={file_info} bytes, is_dir={is_dir}\n"
    return final_response
        
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
