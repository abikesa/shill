#!/usr/bin/env python3

import os
import random
import string
import subprocess
from datetime import datetime

BASE_DIR = '../../..'  # Adjust as needed

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

def git_commit(filepath, message):
    try:
        subprocess.run(["git", "add", filepath], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")

def plant_flicks(base_dir):
    count = 0
    for root, dirs, files in os.walk(base_dir):
        try:
            flick_path = flick_file_path(root)
            with open(flick_path, 'a') as f:
                graffiti = random_graffiti()
                f.write(graffiti)

            rel_path = os.path.relpath(flick_path, base_dir)
            git_commit(flick_path, f"Flicked {rel_path}: {graffiti.strip()}")
            count += 1
        except Exception as e:
            print(f"❌ Failed in {root}: {e}")
    print(f"✅ Flicked and committed {count} folders.")

if __name__ == '__main__':
    plant_flicks(BASE_DIR)
