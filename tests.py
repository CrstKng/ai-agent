from functions.get_files_info import get_files_info

try:
    a = get_files_info("calculator", ".")
    print(a)
    b = get_files_info("calculator", "pkg")
    print(b)
    c = get_files_info("calculator", "/bin")
    print(c)
    d= get_files_info("calculator", "../")
    print(d)
except Exception as e:
    print(f"Error: {e}")
