import os
from functions.config import MAX_CHARS
from google import genai
from google.genai import types

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
            f'Error: File not found or is not a regular file: "{file_path}"'
        )
    else:
        with open(actual_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            return (
                f"Result for '{file_path}' file: \n"
                f"{file_content_string}...",
                f"[...File '{file_path}' truncated at 10000 characters]"
            )

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the content of a file with a specified file path relative to the working directory, providing file and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to list content from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)