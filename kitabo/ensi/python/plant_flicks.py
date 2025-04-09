#!/usr/bin/env python3
"""
plant_flicks.py 🌱

A ritual script to walk a directory tree, create or append to hidden dotfiles
in each folder, inscribe entropy graffiti, and symbolically mark change.

Each flicked file is optionally added to Git (if available) and a browser can be
opened to the GitHub Pages URL if the repo is public and configured.

Usage:
    python python/plant_flicks.py
"""

import os
import random
import string
from datetime import datetime
import subprocess
import webbrowser

# CONFIG — adjust as needed
BASE_SUBDIR = os.path.join("kitabo", "ensi")   # relative to repo root
GITHUB_PAGES_URL = "https://abikesa.github.io/shill"  # or construct dynamically

# UTILITY FUNCTIONS

def find_git_root(start_dir):
    """Traverse upward to locate the .git directory."""
    current = os.path.abspath(start_dir)
    while current != os.path.dirname(current):
        if os.path.isdir(os.path.join(current, ".git")):
            return current
        current = os.path.dirname(current)
    raise RuntimeError("❌ No .git directory found above this script.")

def random_graffiti():
    """Generates timestamped graffiti string."""
    now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    tag = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return f"# flick {now}-{tag}\n"

def random_filename():
    """Creates a new meaningless hidden filename."""
    base = ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 8)))
    return f".{base}"

def flick_file_path(folder):
    """Choose an existing dotfile to append to, or generate a new one."""
    existing = [f for f in os.listdir(folder) if f.startswith('.') and not f.startswith('..')]
    flicks = [f for f in existing if os.path.isfile(os.path.join(folder, f))]
    if flicks:
        return os.path.join(folder, random.choice(flicks))
    else:
        return os.path.join(folder, random_filename())

def plant_flicks(base_dir, repo_root):
    """Perform the flick ritual: add entropy-bearing marks across folders."""
    count = 0
    for root, _, _ in os.walk(base_dir):
        try:
            flick_path = flick_file_path(root)
            with open(flick_path, 'a') as f:
                f.write(random_graffiti())
            subprocess.run(["git", "-C", repo_root, "add", flick_path], check=True)
            count += 1
        except Exception as e:
            print(f"❌ Failed in {root}: {e}")
    return count

def main():
    try:
        # Step 1: Find the Git repo root
        repo_root = find_git_root(os.getcwd())

        # Step 2: Define the flick locus
        target_dir = os.path.join(repo_root, BASE_SUBDIR)
        if not os.path.exists(target_dir):
            raise FileNotFoundError(f"❌ Target directory does not exist: {target_dir}")

        # Step 3: Ritual flick
        total = plant_flicks(target_dir, repo_root)
        print(f"✅ Flicked {total} folders with symbolic entropy.")

        # Step 4: Open the site
        webbrowser.open(GITHUB_PAGES_URL)
        print(f"🌐 Opened: {GITHUB_PAGES_URL}")

    except Exception as e:
        print(f"🔥 Ritual failed: {e}")

if __name__ == '__main__':
    main()
