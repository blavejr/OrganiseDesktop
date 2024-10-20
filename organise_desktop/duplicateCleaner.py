import os
import hashlib

def calculate_file_hash(file_path, block_size=65536):
    """
    Calculate and return MD5 hash of a file for duplicate detection.
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            hash_md5.update(block)
    return hash_md5.hexdigest()

def find_duplicate_files(directory):
    """
    Find and return a dictionary of duplicate files in the directory.
    """
    files_hash_map = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_file_hash(file_path)

            if file_hash in files_hash_map:
                files_hash_map[file_hash].append(file_path)
            else:
                files_hash_map[file_hash] = [file_path]

    duplicates = {hash: paths for hash, paths in files_hash_map.items() if len(paths) > 1}
    return duplicates

def handle_duplicates(duplicates):
    """
    Display duplicate files and ask the user whether to delete them.
    """
    if not duplicates:
        print("No duplicates found.")
        return

    print("Duplicate files found:")
    for hash_value, file_paths in duplicates.items():
        print(f"\nHash: {hash_value}")
        for i, file_path in enumerate(file_paths, 1):
            print(f"{i}. {file_path}")

        delete = input(f"\nDo you want to delete duplicates for hash {hash_value}? (yes/no): ").strip().lower()
        if delete == 'yes':
            for file_path in file_paths[1:]:
                try:
                    print(f"Deleting {file_path}...")
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    print("Duplicate file cleanup complete.")

def clean_duplicates(directory):
    """
    Main function to clean duplicates in the given directory.
    """
    duplicates = find_duplicate_files(directory)
    handle_duplicates(duplicates)
