#!/usr/bin/env python3
"""
plant_flicks.py 🌱

A script to perform the flick ritual: dropping entropy-bearing dotfiles into each directory 
within a given subtree, symbolically marking presence, randomness, and change. 
Each file is added to Git using the correct repository root.

This is not just utility—it's epistemology in motion.

Usage:
    python python/plant_flicks.py
"""

import os
import subprocess
import random
import string
import webbrowser
import sys

def find_git_root(start_dir):
    """
    Recursively traverse upward from the start_dir to locate the Git root.
    
    Parameters:
        start_dir (str): The directory from which to start the search.

    Returns:
        str: Absolute path to the root of the Git repository.

    Raises:
        RuntimeError: If no .git directory is found.
    """
    current = os.path.abspath(start_dir)
    while current != os.path.dirname(current):
        if os.path.isdir(os.path.join(current, ".git")):
            return current
        current = os.path.dirname(current)
    raise RuntimeError("❌ No .git directory found above this script.")

def random_dotfile_name():
    """
    Generates a pseudo-random dotfile name using lowercase letters.

    Returns:
        str: A string like '.xajwqptz'
    """
    name = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f".{name}"

def flick_entropy_into_folders(base_dir, repo_root):
    """
    Walks through all directories starting from base_dir,
    creates a hidden entropy dotfile in each folder,
    and adds it to Git using -C repo_root.

    Parameters:
        base_dir (str): The base directory to walk through.
        repo_root (str): The root directory of the Git repository.

    Returns:
        int: Number of entropy files successfully added.
    """
    entropy_count = 0

    for root, dirs, _ in os.walk(base_dir):
        for d in dirs:
            dir_path = os.path.join(root, d)
            dotfile = os.path.join(dir_path, random_dotfile_name())

            try:
                with open(dotfile, "w") as f:
                    f.write("entropy\n")
                subprocess.run(["git", "-C", repo_root, "add", dotfile], check=True)
                entropy_count += 1
            except subprocess.CalledProcessError as e:
                print(f"❌ Git error on {dotfile}: {e}")
            except Exception as e:
                print(f"⚠️ Unexpected error in {dir_path}: {e}")

    return entropy_count

def open_built_html(repo_root):
    """
    Opens the rendered Jupyter Book index.html in the default browser.
    """
    index_path = os.path.join(repo_root, "shill", "kitabo", "ensi", "_build", "html", "index.html")
    if os.path.exists(index_path):
        webbrowser.open(f"file://{index_path}")
    else:
        print("⚠️ No HTML index found to open.")

def main():
    """
    Entry point for the flick ritual.
    """
    try:
        repo_root = find_git_root(os.getcwd())
        target_dir = os.path.join(repo_root, "shill", "kitabo", "ensi")

        if not os.path.exists(target_dir):
            raise FileNotFoundError(f"❌ Target directory does not exist: {target_dir}")

        total = flick_entropy_into_folders(target_dir, repo_root)
        print(f"✅ Flick ritual complete. {total} folders received entropy.")

        open_built_html(repo_root)

    except Exception as e:
        print(f"🔥 Ritual failed: {e}")

if __name__ == "__main__":
    main()
