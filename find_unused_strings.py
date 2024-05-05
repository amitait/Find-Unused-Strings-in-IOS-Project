import os

# Relative paths from the script's location
strings_file_path = 'en.lproj/Localizable.strings'  # Adjust if needed
source_directory = './'  # Represents the current directory where the script is located

def extract_keys(strings_file):
    keys = set()
    try:
        with open(strings_file, 'r', encoding='utf-16') as file:  # Adjusted for UTF-16 encoding
            for line in file:
                if '"' in line:
                    key = line.split('"')[1]
                    keys.add(key)
    except UnicodeDecodeError:
        print("Error decoding the .strings file. Please check the file's encoding.")
    return keys

def find_unused_keys(keys, source_dir):
    unused_keys = keys.copy()
    for subdir, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.swift') or file.endswith('.m'):
                filepath = os.path.join(subdir, file)
                with open(filepath, 'r', encoding='utf-8') as code_file:  # Assuming source files are UTF-8
                    file_content = code_file.read()
                    for key in keys:
                        if key in file_content:
                            unused_keys.discard(key)
                            if not unused_keys:  # Early exit if all keys are found
                                return unused_keys
    return unused_keys

def main():
    keys = extract_keys(strings_file_path)
    unused_keys = find_unused_keys(keys, source_directory)
    if unused_keys:
        print("Unused keys:")
        for key in unused_keys:
            print(key)
    else:
        print("No unused keys found.")

if __name__ == "__main__":
    main()
