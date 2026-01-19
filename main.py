import os
import sys
from dotenv import load_dotenv
from obsidian_sync import sync_single_file

load_dotenv()
VAULT_PATH = os.getenv("VAULT_PATH")

def main():
    print("=== Obsidian → Notion File Transfer ===\n")

    if not VAULT_PATH or not os.path.isdir(VAULT_PATH):
        print(f" VAULT_PATH invalid: {VAULT_PATH}")
        return

    # Check if any file arguments are passed
    if len(sys.argv) < 2:
        print("Usage: python main.py <file1> <file2> ...")
        print("Example: python main.py 'Project Brief.md' 'Resume.md'")
        return

    files_to_send = sys.argv[1:]
    notes_sent = 0

    for f in files_to_send:
        # Construct full path if user gives relative filename
        file_path = os.path.join(VAULT_PATH, f) if not os.path.isabs(f) else f

        if not os.path.isfile(file_path):
            print(f" File not found: {file_path}")
            continue

        result = sync_single_file(file_path)
        notes_sent += result

    print(f"\n Finished! {notes_sent} files sent to Notion.")

if __name__ == "__main__":
    main()
