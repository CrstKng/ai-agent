import os
from google import genai
from google.genai import types


def get_files_info(working_directory, directory):
    actual_dir = os.path.join(working_directory, directory) #why do I need this fix???
    abs_directory = os.path.abspath(actual_dir) 
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_directory.startswith(abs_working_directory):
        return(
            f"Result for '{directory}' directory: \n"
            f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        )
    elif not os.path.isdir(actual_dir):
        return (
            f"Result for '{directory}' directory: \n"
            f'Error: "{directory}" is not a directory'
        )
    else:
        file_path = os.path.join(abs_working_directory, directory)
        contents_dir = os.listdir(abs_directory)
        described_contents = []
        for content in contents_dir:
            described_contents.append((f"- {content}: file_size={os.path.getsize(file_path)} bytes, is_dir={not os.path.isfile(content)}"))
        final_description = "\n".join(described_contents)
        if directory == ".":
            return (
                "Result for current directory: \n"
                f'{final_description}'
            )
        else:
            return (
                f"Result for '{directory}' directory: \n"
                f'{final_description}'
            )
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)