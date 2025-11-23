import os
import subprocess

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
            f'Error: File "{file_path}" not found.'
        )
    else:
        all_args = ["uv", "run", f"{actual_file}"]
        all_args += args
        try:
            completed_process = subprocess.run(all_args, timeout = 30, capture_output = True)
        except Exception as e:
            return(f"Error: executing Python file: {e}")
        return(
            f"Result for '{actual_file}' file: \n"
            f'STDOUT: {completed_process.stdout} \n'
            f'STDERR: {completed_process.stderr}'
        )
        if not completed_process.returncode == 0:
            return(
                f"Result for '{actual_file}' file: \n"
                f'Process exited with code {completed_process.returncode}'
            )
        if completed_process.output == None:
            return(
                f"Result for '{actual_file}' file: \n"
                f'No output produced.'
            )