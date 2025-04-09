#!/usr/bin/env python3
"""
plant_flicks.py 🌱

Walks the directory tree from a base, drops graffiti-bearing dotfiles,
and commits each one independently, rooted at the top-level Git repo.

Usage:
    python python/plant_flicks.py
"""

import os
import random
import string
from datetime import datetime
import subprocess

# Dynamically locate Git root
def find_git_root(start_path="."):
    path = os.path.abspath(start_path)
    while path != "/":
        if os.path.isdir(os.path.join(path, ".git")):
            return path
        path = os.path.dirname(path)
    raise RuntimeError("❌ Git root not found.")

# Random graffiti tag
def random_tag():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=4))

# Random dotfile
def random_filename():
    return f".{''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 8)))}"

# The flick mark
def generate_graffiti():
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    tag = random_tag()
    return f"# flick {timestamp}-{tag}\n"

# Choose a file to flick (existing or new)
def get_or_create_flick_path(folder):
    hidden = [f for f in os.listdir(folder) if f.startswith('.') and not f.startswith('..')]
    dotfiles = [f for f in hidden if os.path.isfile(os.path.join(folder, f))]
    if dotfiles:
        return os.path.join(folder, random.choice(dotfiles))
    else:
        return os.path.join(folder, random_filename())

# Add and commit from the top-level git root
def git_commit(repo_root, file_path, message):
    try:
        subprocess.run(["git", "-C", repo_root, "add", file_path], check=True)
        subprocess.run(["git", "-C", repo_root, "commit", "-m", message], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Git commit failed for {file_path}: {e}")

# Main ritual
def plant_flicks(base_dir):
    repo_root = find_git_root(base_dir)
    print(f"🌲 Git root found at: {repo_root}\n")

    flicked = 0
    for root, dirs, _ in os.walk(base_dir):
        try:
            flick_path = get_or_create_flick_path(root)
            with open(flick_path, 'a') as f:
                graffiti = generate_graffiti()
                f.write(graffiti)
            rel_path = os.path.relpath(flick_path, start=repo_root)
            commit_msg = f"🌱 flicked {rel_path}"
            git_commit(repo_root, rel_path, commit_msg)
            print(f"✅ {commit_msg}")
            flicked += 1
        except Exception as e:
            print(f"❌ Failed in {root}: {e}")
    print(f"\n🌿 Ritual complete: {flicked} folders flicked.")

if __name__ == "__main__":
    plant_flicks("../../../")
