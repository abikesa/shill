#!/usr/bin/env python3

import os
import random
import string
import subprocess
from datetime import datetime

# 📍 Get absolute path to the root of the Git repo
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))

# 🎨 Generates a random graffiti string with timestamp + tag
def random_graffiti():
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    tag = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    phrase = random.choice([
        "entropy lives here",
        "a whisper in the branch",
        "this folder has been flicked",
        "signed by static electricity",
        "noise is not error",
        "entropy is a feature",
        "👣 trace of a ghost",
        "🌀 flick and be gone",
        "⛓️ semantically meaningless",
        "🌊 washed ashore",
        "🖋️ signed by no one"
    ])
    return f"# flick {now} — {tag} — {phrase}\n"

# 🕳️ Generates a random hidden filename
def random_filename():
    base = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 9)))
    return f".{base}"

# 📂 Picks or creates a flick file in a folder
def flick_file_path(folder):
    try:
        existing = [f for f in os.listdir(folder) if f.startswith('.') and not f.startswith('..')]
        flicks = [f for f in existing if os.path.isfile(os.path.join(folder, f))]
        if flicks:
            return os.path.join(folder, random.choice(flicks))
        else:
            return os.path.join(folder, random_filename())
    except Exception:
        return os.path.join(folder, random_filename())

# 🧷 Stages and commits a single file with poetry
def git_commit(abs_path, graffiti):
    rel_path = os.path.relpath(abs_path, REPO_ROOT)
    commit_message = f"🌱 flicked `{rel_path}` — {graffiti.strip()}"
    try:
        subprocess.run(["git", "-C", REPO_ROOT, "add", rel_path], check=True)
        subprocess.run(["git", "-C", REPO_ROOT, "commit", "-m", commit_message], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error on {rel_path}: {e}")

# 🌳 Main flicking function
def plant_flicks(base_dir):
    print(f"🌿 Starting flicking ritual in: {base_dir}")
    count = 0
    for root, dirs, files in os.walk(base_dir):
        if ".git" in root:
            continue  # 🚫 Skip Git internals
        try:
            flick_path = flick_file_path(root)
            graffiti = random_graffiti()
            with open(flick_path, 'a') as f:
                f.write(graffiti)
            git_commit(flick_path, graffiti)
            count += 1
        except Exception as e:
            print(f"⚠️  Failed to flick `{root}`: {e}")
    print(f"✅ Flicked and committed {count} folders. The ritual is complete.")

if __name__ == '__main__':
    plant_flicks(REPO_ROOT)
