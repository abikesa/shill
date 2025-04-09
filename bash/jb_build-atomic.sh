#!/bin/bash

# Prompt for a commit message
echo "Enter your commit message:"
read commit_message

# Optional: deactivate virtual env (useful on older setups)
if [ -f "../../../myenv/bin/deactivate" ]; then
  source ../../../myenv/bin/deactivate
fi

# Step 1: Clean previous builds
jb clean .

# Step 2: Build the Jupyter Book
jb build .

# Step 3: Run additional cleaning
bash/jb_clean.sh

# Step 4: Import HTML to gh-pages
ghp-import -n -p -f _build/html
if [ $? -ne 0 ]; then
  echo "❌ ghp-import failed. Aborting flick ritual."
  exit 1
fi

# Step 5: Return to Git root
cd ../..

# Step 6: Stage and commit main content
git add .
git commit -m "$commit_message"

# Step 7: Push core content
git push

# Step 8: Run flick ritual (separate graffiti & commit per flick)
python "$(dirname "$0")/../python/plant_flicks.py"
