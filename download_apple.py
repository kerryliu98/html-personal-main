import os
import shutil
import subprocess
import urllib.request

def ensure_wget():
    if not os.path.exists("wget.exe"):
        print("Downloading wget.exe...")
        url = "https://eternallybored.org/misc/wget/1.21.4/64/wget.exe"
        urllib.request.urlretrieve(url, "wget.exe")
        print("wget.exe downloaded.")

def clone_site():
    print("Cloning Apple CA website...")
    # Clean previous download directory if it exists
    if os.path.exists("www.apple.com"):
        shutil.rmtree("www.apple.com")
        
    subprocess.run(["wget.exe", "-p", "-k", "-E", "-H", "https://www.apple.com/ca/"], check=False)

def move_and_patch():
    print("Moving files and patching paths...")
    src_dir = "www.apple.com"
    if not os.path.exists(src_dir):
        print("Download failed, www.apple.com folder not found.")
        return

    dest_dir = "."

    # Move folders out of www.apple.com
    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(dest_dir, item)
        if os.path.exists(d):
            if os.path.isdir(d):
                shutil.rmtree(d)
            else:
                os.remove(d)
        shutil.move(s, d)

    # Remove now empty www.apple.com
    if os.path.exists(src_dir):
        shutil.rmtree(src_dir)

    # Patch index.html
    html_path = "ca/index.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Fix links that went up one level
        content = content.replace('href="../', 'href="./')
        content = content.replace('src="../', 'src="./')
        # Fix relative links that stayed within ca/
        content = content.replace('href="home/', 'href="ca/home/')
        content = content.replace('src="home/', 'src="ca/home/')
        content = content.replace('url("home/', 'url("ca/home/')

        with open("apple_test.html", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("Successfully created apple_test.html with local resources.")

if __name__ == "__main__":
    ensure_wget()
    clone_site()
    move_and_patch()
