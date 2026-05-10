import os
import shutil
import subprocess
import urllib.request
import re

def ensure_wget():
    # Use wget from the current directory or download it
    if not os.path.exists("wget.exe"):
        print("Downloading wget.exe...")
        url = "https://eternallybored.org/misc/wget/1.21.4/64/wget.exe"
        urllib.request.urlretrieve(url, "wget.exe")
        print("wget.exe downloaded.")

def clone_site():
    print("Cloning Google CA website...")
    # Clean previous attempts
    for folder in ["www.google.ca", "google.ca"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    # Download the page
    subprocess.run(["wget.exe", "-p", "-k", "-E", "-H", "https://www.google.ca/"], check=False)

def move_and_patch():
    print("Processing files...")
    # Wget creates folders based on domain names
    src_dirs = ["www.google.ca", "google.ca"]
    src_dir = next((d for d in src_dirs if os.path.exists(d)), None)
    
    if not src_dir:
        print("Download failed, source folder not found.")
        return

    # Move files from the domain folder to the current directory (google/)
    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(".", item)
        if os.path.exists(d):
            if os.path.isdir(d): shutil.rmtree(d)
            else: os.remove(d)
        shutil.move(s, d)
    
    shutil.rmtree(src_dir)

    # Move all other downloaded host folders (gstatic, etc.) into the google folder
    # These are currently in the parent directory because we are running from google/
    parent_dir = ".."
    for item in os.listdir(parent_dir):
        item_path = os.path.join(parent_dir, item)
        # Only move directories that look like domains (have a dot, don't start with a dot)
        if os.path.isdir(item_path) and "." in item and not item.startswith(".") and item not in ["apple", "temp", "google"]:
            dest_path = os.path.join(".", item)
            if os.path.exists(dest_path): shutil.rmtree(dest_path)
            try:
                shutil.move(item_path, dest_path)
            except Exception as e:
                print(f"Could not move {item}: {e}")

    # Patch index.html
    html_path = "index.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # 1. Remove "Google offered in: Français" or language switchers
        content = re.sub(r'<div[^>]*?>Google offered in:.*?</div>', '', content)
        content = re.sub(r'<div[^>]*?id="SIvCob"[^>]*?>.*?</div>', '', content) # Specific Google ID for language links
        
        # 2. Remove alternate links
        content = re.sub(r'<link rel="alternate" [^>]*>', '', content)

        # 3. Remove blank rows
        content = re.sub(r'(\n\s*){3,}', '\n\n', content).lstrip()

        with open("google_test.html", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("Successfully created google_test.html with local resources.")

if __name__ == "__main__":
    # Ensure we have wget.exe here
    if not os.path.exists("wget.exe") and os.path.exists("../apple/wget.exe"):
        shutil.copy("../apple/wget.exe", "wget.exe")
    
    ensure_wget()
    clone_site()
    move_and_patch()
