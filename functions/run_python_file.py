import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    actual_file = os.path.join(working_directory, file_path) #why do I need this fix???
    abs_directory = os.path.abspath(actual_file) 
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_directory.startswith(abs_working_directory):
        return(
            f"Result for '{actual_file}' file: \n"
            f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        )
    divided_input = actual_file.split("/")
    file_name = divided_input[-1]
    if not file_name.endswith('.py'):
        return(
            f"Result for '{actual_file}' file: \n"
            f'Error: "{file_path}" is not a Python file.'
        )
    elif not os.path.exists(abs_directory):
        return (
            f"Result for '{actual_file}' file: \n"
            f'Error: File "{file_path}" does not exist or is not a regular file.'
        )
    else:
        all_args = ["uv", "run", f"{actual_file}"]
        all_args += args
        try:
            completed_process = subprocess.run(all_args, timeout = 30, capture_output = True)
        except Exception as e:
            return(f"Error: executing Python file: {e}")
        if not completed_process.returncode == 0:
            return(
                f"Result for '{actual_file}' file: \n"
                f'Process exited with code {completed_process.returncode}'
            )
        if completed_process.stdout and completed_process.stderr is None:
            return(
                f"Result for '{actual_file}' file: \n"
                f'No output produced.'
            )
        return(
            f"Result for '{actual_file}' file: \n"
            f'STDOUT: {completed_process.stdout} \n'
            f'STDERR: {completed_process.stderr}'
        )

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file in a specified directory relative to the working directory, providing the output generated from that execution",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to execute files from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of all voluntary additional arguments.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A voluntary additional argument."
                ),
            ),
        },
        required=["file_path"],
    ),
)