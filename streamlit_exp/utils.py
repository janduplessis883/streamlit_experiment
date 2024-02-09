import os
import time
from colorama import Fore, init, Style

init(autoreset=True)


# Decorators --------------------------------------------------------
def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"{Fore.YELLOW}[▶️] FUCTION: {func.__name__}()")
        result = func(*args, **kwargs)
        print(
            f"{Fore.GREEN}{Style.DIM}[✅] Completed: {func.__name__}() - Time taken: {time.time() - start_time:.2f} seconds"
        )
        return result

    return wrapper


# General Utils -----------------------------------------------------
def list_all_files(dir_path):
    files = []
    for root, dirs, file_names in os.walk(dir_path):
        for file_name in file_names:
            files.append(file_name)

    for f in files:
        print(f)
