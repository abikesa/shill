#!/usr/bin/env python3

import os
import random
import string
from datetime import datetime

# Base directory to walk through
BASE_DIR = '../../../'  # change if needed

# Graffiti generator
def random_graffiti():
    now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    tag = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return f"# flick {now}-{tag}\n"

# Random meaningless filename generator (hidden file)
def random_filename():
    base = ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 8)))
    return f".{base}"

# Adds or updates a flick file in the given folder
def flick_file_path(folder):
    existing = [f for f in os.listdir(folder) if f.startswith('.') and not f.startswith('..')]
    flicks = [f for f in existing if os.path.isfile(os.path.join(folder, f))]
    if flicks:
        return os.path.join(folder, random.choice(flicks))  # Append to an existing one
    else:
        return os.path.join(folder, random_filename())  # Create a new one

def plant_flicks(base_dir):
    count = 0
    for root, dirs, files in os.walk(base_dir):
        try:
            flick_path = flick_file_path(root)
            with open(flick_path, 'a') as f:
                f.write(random_graffiti())
            count += 1
        except Exception as e:
            print(f"❌ Failed in {root}: {e}")
    print(f"✅ Flicked {count} folders with random noise.")

if __name__ == '__main__':
    plant_flicks(BASE_DIR)
