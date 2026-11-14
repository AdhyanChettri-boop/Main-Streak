import os
import shutil
from pathlib import Path

# Define categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp"],
}

def organize_folder(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print("Folder does not exist!")
        return

    for file in folder.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            moved = False

            for category, extensions in FILE_TYPES.items():
                if ext in extensions:
                    target_dir = folder / category
                    target_dir.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target_dir / file.name))
                    print(f"Moved: {file.name} → {category}/")
                    moved = True
                    break

            if not moved:
                other_dir = folder / "Others"
                other_dir.mkdir(exist_ok=True)
                shutil.move(str(file), str(other_dir / file.name))
                print(f"Moved: {file.name} → Others/")

if __name__ == "__main__":
    path = input("Enter folder path to organize: ").strip()
    organize_folder(path)
    print("\nDone!")
