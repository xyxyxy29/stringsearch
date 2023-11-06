#!/usr/bin/env python3

import os
import sys
import fnmatch
import re
from colorama import Fore, Style, init

# ASCII art for "stringsearch"
ascii_art = """
 ____  _        _             ____                      _                   
/ ___|| |_ _ __(_)_ __   __ _/ ___|  ___  __ _ _ __ ___| |__    _ __  _   _ 
\___ \| __| '__| | '_ \ / _` \___ \ / _ \/ _` | '__/ __| '_ \  | '_ \| | | |
 ___) | |_| |  | | | | | (_| |___) |  __/ (_| | | | (__| | | |_| |_) | |_| |
|____/ \__|_|  |_|_| |_|\__, |____/ \___|\__,_|_|  \___|_| |_(_) .__/ \__, |
                        |___/                                  |_|    |___/ 

v1.0
"""

# Print ASCII art
print(Fore.WHITE + Style.BRIGHT + ascii_art + Style.RESET_ALL)


# Initialize colorama
init()

# Check for the correct number of command line arguments
if len(sys.argv) != 3:
    script_path = os.path.basename(sys.argv[0])
    print("Usage: python",script_path, "<search_path> <search_string>")
    sys.exit(1)

search_string = sys.argv[2]
path = sys.argv[1]

# Function to highlight matches in a line
def highlight_matches(line, line_number):
    highlighted_line = re.sub(search_string, Fore.RED + Style.BRIGHT + r'\g<0>' + Style.RESET_ALL, line, flags=re.IGNORECASE)
    return f"Line {line_number}: {highlighted_line}"

# Function to search for the given string in a file
def search_in_file(file_path, filename):
    try:
        with open(file_path, 'r', errors='ignore') as file:
            matches_found = False
            for line_number, line in enumerate(file, start=1):
                if re.search(search_string, line, flags=re.IGNORECASE):
                    if not matches_found:
                        print(Fore.RED + Style.BRIGHT + "\n[ MATCH FOUND ]" + Style.RESET_ALL)
                        matches_found = True
                        print(Fore.RED + Style.BRIGHT + f".\\{filename}" + Style.RESET_ALL)
                    print(highlight_matches(line, line_number), end="")
    except (IOError, UnicodeDecodeError):
        pass  # Ignore errors for unreadable files or invalid encoding

# Recursively search for files in the current directory and its subdirectories
for root, _, files in os.walk(path):
    for filename in fnmatch.filter(files, '*'):
        file_path = os.path.join(root, filename)
        search_in_file(file_path, filename)
