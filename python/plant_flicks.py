#!/usr/bin/env python3

import os
import random
import string
import subprocess
from datetime import datetime

# Get absolute path to the repo root (shill/)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))

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

def git_commit(abs_path, message):
    rel_path = os.path.relpath(abs_path, REPO_ROOT)
    try:
        subprocess.run(["git", "-C", REPO_ROOT, "add", rel_path], check=True)
        subprocess.run(["git", "-C", REPO_ROOT, "commit", "-m", message], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Git commit failed for {rel_path}: {e}")

def plant_flicks(base_dir):
    count = 0
    for root, dirs, files in os.walk(base_dir):
        try:
            flick_path = flick_file_path(root)
            with open(flick_path, 'a') as f:
                graffiti = random_graffiti()
                f.write(graffiti)

            git_commit(flick_path, f"flick: {os.path.relpath(flick_path, REPO_ROOT)} — {graffiti.strip()}")
            count += 1
        except Exception as e:
            print(f"❌ Failed in {root}: {e}")
    print(f"✅ Flicked and committed {count} folders.")

if __name__ == '__main__':
    plant_flicks(REPO_ROOT)
