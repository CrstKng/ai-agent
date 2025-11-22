import os
from functions.config import MAX_CHARS


def write_file(working_directory, file_path, content):
    actual_file = os.path.join(working_directory, file_path) #why do I need this fix???
    abs_directory = os.path.abspath(actual_file) 
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_directory.startswith(abs_working_directory):
        return(
            f"Result for '{file_path}' file: \n"
            f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        )
    divided_input = actual_file.split("/")
    actual_dir = "/".join(divided_input[:-1])
    if not os.path.exists(os.path.abspath(actual_dir)):
        os.makedirs(actual_dir)
        return (
            f"Result for '{file_path}' file: \n"
            f'Error: "{file_path}" is not a file \n'
            f'Tried to create {file_path}'
        )
    else:
        with open(actual_file, "w") as f:
            f.write(content)
            return(
                f"Result for '{file_path}' file: \n"
                f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            )
