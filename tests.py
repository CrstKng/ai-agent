from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

try:
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
except Exception as e:
    print(f"Error: {e}")
