import os
import shutil
from datetime import datetime

# Customize these paths
TARGET_FOLDERS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Godzilla"),
]
DEST_DIR = os.path.expanduser("~/Desktop/Scripts/Organized")
BACKUP_DIR = os.path.expanduser("~/Desktop/Scripts/Backups")

# Define file type categories
CATEGORIES = {
    "Documents": ["pdf", "doc", "docx", "txt", "md", "odt"],
    "Images": ["jpg", "jpeg", "png", "gif", "bmp", "svg"],
    "Videos": ["mp4", "mkv", "mov", "avi"],
    "Music": ["mp3", "wav", "flac"],
    "Archives": ["zip", "rar", "tar", "gz", "7z"],
    "Code": ["py", "cpp", "c", "java", "js", "html", "css", "sh"],
}

def create_folders():
    os.makedirs(DEST_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    for category in CATEGORIES:
        os.makedirs(os.path.join(DEST_DIR, category), exist_ok=True)
    os.makedirs(os.path.join(DEST_DIR, "Others"), exist_ok=True)

def move_file(file_path):
    ext = file_path.split('.')[-1].lower()
    destination = "Others"
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            destination = category
            break
    shutil.move(file_path, os.path.join(DEST_DIR, destination, os.path.basename(file_path)))

def organize_all():
    for folder in TARGET_FOLDERS:
        for filename in os.listdir(folder):
            full_path = os.path.join(folder, filename)
            if os.path.isfile(full_path):
                # Skip organizing script itself
                if "organizer" in filename.lower():
                    continue
                # Delete logs and tmp files
                if filename.endswith((".log", ".tmp")):
                    os.remove(full_path)
                else:
                    move_file(full_path)

def backup():
    time_tag = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = os.path.join(BACKUP_DIR, f"backup_{time_tag}")
    shutil.copytree(DEST_DIR, backup_path)

def main():
    print("🚀 Organizing files...")
    create_folders()
    organize_all()
    backup()
    print("✅ Done! Files organized and backed up.")

if __name__ == "__main__":
    main()
