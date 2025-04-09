#!/usr/bin/env python3

import os
import random
import string
import subprocess
from datetime import datetime

# Set this to your actual base directory (adjust as needed)
BASE_DIR = os.path.abspath("../../../")

def random_graffiti():
    now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    tag = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return f"# flick {now}-{tag}\n"

def random_filename():
    base = ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 8)))
    return f".{base}"

def flick_file_path(folder):
    existing = [f for f in os.listdir(folder) if f.startswith('.') and not f.startswith('..')]
    flicks = [f for f in existing if os.path.isfile(os.path.join(folder, f))]
    if flicks:
        return os.path.join(folder, random.choice(flicks))
    else:
        return os.path.join(folder, random_filename())

def find_git_root(start_dir):
    current = os.path.abspath(start_dir)
    while current != os.path.dirname(current):
        if os.path.isdir(os.path.join(current, ".git")):
            return current
        current = os.path.dirname(current)
    raise RuntimeError("❌ No .git directory found")

def plant_and_commit_flicks(base_dir):
    repo_root = find_git_root(base_dir)
    count = 0
    for root, dirs, files in os.walk(base_dir):
        try:
            flick_path = flick_file_path(root)
            graffiti = random_graffiti()
            with open(flick_path, 'a') as f:
                f.write(graffiti)

            rel_path = os.path.relpath(flick_path, repo_root)
            subprocess.run(["git", "-C", repo_root, "add", rel_path], check=True)
            subprocess.run(["git", "-C", repo_root, "commit", "-m", graffiti.strip()], check=True)
            count += 1
        except Exception as e:
            print(f"❌ Failed in {root}: {e}")
    print(f"✅ Individually committed flicks in {count} folders.")

if __name__ == "__main__":
    plant_and_commit_flicks(BASE_DIR)
