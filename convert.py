import os
import re

def replace_paths_in_file(file_path):
    # Regular expression to match the file paths in the format r'xxx\yyy'
    path_pattern = re.compile(r"r'([^']+)'")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find all matches of the pattern
    paths = path_pattern.findall(content)
    
    if not paths:
        return
    
    # Add import os if not already present
    if 'import os' not in content:
        content = 'import os\n' + content

    # Replace each found path with os.path.join format
    for path in paths:
        # Replace backslashes and slashes with commas and double quotes
        path_parts = re.split(r'[\\/]', path)
        joined_path = 'os.path.join({})'.format(', '.join(['"{}"'.format(part) for part in path_parts]))
        # Replace the original raw string path with the new joined path
        content = content.replace(f"r'{path}'", joined_path)

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                replace_paths_in_file(file_path)

# Specify the directory to process
directory_to_process = './loop_module/'

process_directory(directory_to_process)
