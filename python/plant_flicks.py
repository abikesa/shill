#!/usr/bin/env python3

import os
import subprocess
import webbrowser
import sys

# -----------------------------------------------------------------------------
# Helper function: Find the git repo root by traversing upward from a path
def find_git_root(start_path):
    current = start_path
    while True:
        if os.path.isdir(os.path.join(current, ".git")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            raise RuntimeError("Reached filesystem root. No .git directory found.")
        current = parent

# -----------------------------------------------------------------------------
# Main execution

if __name__ == "__main__":
    # Location of this script
    HERE = os.path.dirname(os.path.abspath(__file__))

    # Find the top-level Git directory from script's location
    REPO_ROOT = find_git_root(HERE)

    # Construct absolute path to the `kitabo/ensi` directory
    TARGET = os.path.join(REPO_ROOT, "kitabo", "ensi")

    # Optional: change working directory to where jb expects to run
    os.chdir(TARGET)

    # Run jupyter-book build
    subprocess.run(["jb", "build", "."], check=True)

    # Open the resulting HTML in default browser
    output_path = os.path.join(TARGET, "_build", "html", "index.html")
    if not os.path.exists(output_path):
        print(f"❌ Failed: {output_path} not found")
        sys.exit(1)

    print(f"\n✅ Opening: {output_path}")
    webbrowser.open(f"file://{output_path}")
