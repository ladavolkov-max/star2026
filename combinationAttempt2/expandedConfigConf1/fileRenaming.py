
def remove_lines_starting_with(file_path, prefix):
    # 1. Read all lines from the original file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # 2. Filter out lines that start with the specific prefix
    filtered_lines = [line for line in lines if not line.startswith(prefix)]
    
    # 3. Write the filtered lines back to overwrite the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(filtered_lines)

# --- Example Usage ---
# Suppose you have a file named 'data.txt' and want to remove lines starting with '#'
target_file = './batch99.txt'
prefix_to_remove = 'trial'

remove_lines_starting_with(target_file, prefix_to_remove)
print(f"Successfully processed '{target_file}'.")
