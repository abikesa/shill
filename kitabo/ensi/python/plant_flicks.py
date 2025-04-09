#!/usr/bin/env python3

import os
import random
import string
import subprocess
from datetime import datetime

# 🤓 You are calling this from: shill/kitabo/ensi/
# So the Git root is: ../../..
REPO_ROOT = os.path.abspath(os.path.join(os.getcwd(), "../../.."))

EXCLUDE_DIRS = {
    '.git', 'myenv', '__pycache__', '.venv', 'env', 'site-packages', 'node_modules', '.mypy_cache'
}

def random_graffiti():
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    tag = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    phrase = random.choice([
        "echo from entropy",
        "mark of meaninglessness",
        "signed by the void",
        "ripple in the repo",
        "trace of recursion",
        "👁️ whisper from the abyss",
        "📜 stamped and forgotten",
        "🌀 data with no witness"
    ])
    return f"# flick {now} — {tag} — {phrase}\n"

def random_filename():
    return "." + ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 9)))

def flick_file_path(folder):
    try:
        flicks = [f for f in os.listdir(folder)
                  if f.startswith('.') and not f.startswith('..')
                  and os.path.isfile(os.path.join(folder, f))]
        if flicks:
            return os.path.join(folder, random.choice(flicks))
        else:
            return os.path.join(folder, random_filename())
    except Exception:
        return os.path.join(folder, random_filename())

def git_commit(abs_path, graffiti):
    rel_path = os.path.relpath(abs_path, REPO_ROOT)
    msg = f"🌱 flicked `{rel_path}` — {graffiti.strip()}"
    try:
        subprocess.run(["git", "-C", REPO_ROOT, "add", rel_path], check=True)
        subprocess.run(["git", "-C", REPO_ROOT, "commit", "-m", msg], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error on {rel_path}: {e}")

def is_valid_folder(path):
    for part in path.split(os.sep):
        if part in EXCLUDE_DIRS:
            return False
    return True

def plant_flicks(base_dir):
    print(f"🌿 Initiating flick ritual from {base_dir}")
    count = 0
    for root, dirs, files in os.walk(base_dir):
        if not is_valid_folder(root):
            continue
        try:
            flick_path = flick_file_path(root)
            graffiti = random_graffiti()
            with open(flick_path, 'a') as f:
                f.write(graffiti)
            git_commit(flick_path, graffiti)
            count += 1
        except Exception as e:
            print(f"⚠️  Failed to flick {root}: {e}")
    print(f"✅ Flick ritual complete. {count} folders received entropy.")

if __name__ == '__main__':
    plant_flicks(REPO_ROOT)
