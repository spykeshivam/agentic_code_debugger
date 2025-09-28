import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.get_file_content import schema_get_file_content
from functions.call_function import call_function

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    if len(sys.argv) < 2:
        print("Please provide a prompt as a command-line argument.")
        sys.exit(1)
    verbose = False
    if len(sys.argv) > 2 and sys.argv[2] == '--verbose':
        verbose = True
    user_prompt = sys.argv[1]
    system_prompt = """
You are a helpful AI coding agent.

You are in the calculator app working directory.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
    )
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
    )
    max_iters=20
    for i in range(max_iters):

        response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=messages, config=config,
        )
        candidates = response.candidates
        # print(candidates,'###########')
        if response is None or response.usage_metadata is None:
            print('Response or usage metadata is None')
            return
        if verbose:
            print(f"User prompt:{user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            
        if response.candidates:

            print("Function calls in response:",response.function_calls)
            
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)
        if response.function_calls:
            for function_call_part in response.function_calls:
                function_response = call_function(function_call_part, verbose=verbose)
                messages.append(function_response)
        else:
            print(response.text)
            return
        
        
        
        
        print(response.text)
        if response is None or response.usage_metadata is None:
            print('Response or usage metadata is None')
            return
    

# print(get_files_info('calculator','pkg'))
main()