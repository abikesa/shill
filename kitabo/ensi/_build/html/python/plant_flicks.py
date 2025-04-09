#!/usr/bin/env python3
"""
plant_flicks.py 🌱

This script performs the flick ritual: it walks through a directory tree,
drops an entropy-bearing dotfile in each folder, commits each one individually
(with a unique message), and logs the entire ritual to stdout.

Usage:
    python python/plant_flicks.py
"""

import os
import random
import string
from datetime import datetime
import subprocess

# Ritual locus
BASE_DIR = "../../../"  # Adjust if needed

def random_tag():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=4))

def random_filename():
    return f".{''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 8)))}"

def generate_graffiti():
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    tag = random_tag()
    return f"# flick {timestamp}-{tag}\n"

def get_or_create_flick_path(folder):
    existing = [f for f in os.listdir(folder) if f.startswith('.') and not f.startswith('..')]
    flicks = [f for f in existing if os.path.isfile(os.path.join(folder, f))]
    if flicks:
        return os.path.join(folder, random.choice(flicks))  # Append to existing
    else:
        return os.path.join(folder, random_filename())      # Create new

def git_commit(file_path, message):
    try:
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Git commit failed for {file_path}: {e}")

def plant_flicks(base_dir):
    flicked = 0
    for root, dirs, _ in os.walk(base_dir):
        try:
            flick_path = get_or_create_flick_path(root)
            with open(flick_path, 'a') as f:
                graffiti = generate_graffiti()
                f.write(graffiti)
            rel_path = os.path.relpath(flick_path, start=base_dir)
            commit_msg = f"🌱 flicked {rel_path}"
            git_commit(flick_path, commit_msg)
            print(f"✅ {commit_msg}")
            flicked += 1
        except Exception as e:
            print(f"❌ Failed in {root}: {e}")
    print(f"\n🌿 Ritual complete: {flicked} folders received their entropy.")

if __name__ == "__main__":
    plant_flicks(BASE_DIR)
