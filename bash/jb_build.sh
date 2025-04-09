#!/bin/bash

# Prompt for a commit message
echo "Enter your commit message:"
read commit_message

# Wasn't necessarily until 12/2024 upgrade
source ../../../myenv/bin/deactivate

# Clean the Jupyter Book
jb clean .

# Build the Jupyter Book
jb build .

# Run the jb_clean script
bash/jb_clean.sh

# Organized noise: bulletproof path to flick ritual
python "$(dirname "$0")/../../python/plant_flicks.py"

# Import the built HTML to the gh-pages branch
ghp-import -n -p -f _build/html

# Navigate to the root directory of the git repository
cd ../..

# Stage all changes (e.g., new notebooks or structure)
# git add .

# Commit with the user-defined message
# git commit -m "$commit_message"

# Push to remote
git push
