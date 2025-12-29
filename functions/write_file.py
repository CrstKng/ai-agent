import os
from functions.config import MAX_CHARS
from google import genai
from google.genai import types


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

schema_write_files = types.FunctionDeclaration(
    name="write_files",
    description="Writes specified content to a specified file path relative to the working directory, either changing the content of an existing file or creating a new file altogether and writing the content provided in it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="""File path to where a new file will be created or an existing one's content will be changed from, relative to the working directory (default is the working directory itself)""",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the contet we want to write to a new file or rewrite the content in an existing file"
            )
        },
        required=["file_path", "content"]
    ),
)