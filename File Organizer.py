import os
import shutil
import hashlib
from pathlib import Path
from collections import defaultdict

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".7z"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp"],
}

def get_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def organize_files(folder):
    folder = Path(folder)
    for file in folder.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            moved = False
            for category, extensions in FILE_TYPES.items():
                if ext in extensions:
                    target = folder / category
                    target.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target / file.name))
                    print(f"Moved: {file.name} → {category}/")
                    moved = True
                    break
            if not moved:
                other = folder / "Others"
                other.mkdir(exist_ok=True)
                shutil.move(str(file), str(other / file.name))
                print(f"Moved: {file.name} → Others/")

def find_duplicates(folder):
    hashes = defaultdict(list)
    folder = Path(folder)

    for file in folder.rglob("*"):
        if file.is_file():
            file_hash = get_file_hash(file)
            hashes[file_hash].append(file)

    print("\n===== Duplicate Files =====")
    found = False
    for file_list in hashes.values():
        if len(file_list) > 1:
            found = True
            print("\nDuplicates:")
            for f in file_list:
                print(f"  - {f}")
    if not found:
        print("No duplicates found.")

if __name__ == "__main__":
    path = input("Enter folder path: ").strip()
    print("\n1. Organize files")
    print("2. Find duplicates")
    choice = input("Choose: ")

    if choice == "1":
        organize_files(path)
    elif choice == "2":
        find_duplicates(path)
