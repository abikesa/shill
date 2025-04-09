#!/bin/bash

# ──────────────────────────────────────────────────────────────
# 🌊 0. Prompt the navigator
echo "Enter your commit message:"
read commit_message

# ──────────────────────────────────────────────────────────────
# 🚢 1. Optional: deactivate virtual environment (for legacy setups)
if [ -f "../../../myenv/bin/deactivate" ]; then
  source ../../../myenv/bin/deactivate
fi

# ──────────────────────────────────────────────────────────────
# 🪛 2. Clean and rebuild the Jupyter Book
jb clean .
jb build . || { echo "❌ Jupyter Book build failed. Aborting."; exit 1; }

# Optional deeper clean
bash/jb_clean.sh

# ──────────────────────────────────────────────────────────────
# ✂️ 3. Push the built book to `gh-pages` branch
ghp-import -n -p -f _build/html
if [ $? -ne 0 ]; then
  echo "❌ ghp-import failed. Aborting flick ritual."
  exit 1
fi

# ──────────────────────────────────────────────────────────────
# 🦈 4. Return to Git root (bulletproof path)
cd "$(git rev-parse --show-toplevel)" || { echo "❌ Failed to find Git root."; exit 1; }

# ──────────────────────────────────────────────────────────────
# 🛟 5. Plant flicks: the graffiti of discernment
echo "🌿 Planting flicks..."
python "$(git rev-parse --show-toplevel)/kitabo/ensi/python/plant_flicks.py"
if [ $? -ne 0 ]; then
  echo "❌ Flick ritual failed. Proceed with caution."
fi

# Optional: show diff before committing
echo "🧾 Git changes after flicks:"
git diff --stat

# ──────────────────────────────────────────────────────────────
# 🏝️ 6. Stage, commit, and push all content + flicks
git add .
git commit -m "$commit_message"
git push
