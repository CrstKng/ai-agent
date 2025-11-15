import os
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    actual_file = os.path.join(working_directory, file_path) #why do I need this fix???
    abs_directory = os.path.abspath(actual_file) 
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_directory.startswith(abs_working_directory):
        return(
            f"Result for '{file_path}' file: \n"
            f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        )
    elif not os.path.isfile(actual_file):
        return (
            f"Result for '{file_path}' file: \n"
            f'Error: "{file_path}" is not a directory'
        )
    else:
        with open(actual_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            return (
                f"Result for '{file_path}' file: \n"
                f"{file_content_string}...",
                f"[...File '{file_path}' truncated at 10000 characters]"
            )