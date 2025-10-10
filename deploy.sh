#!/bin/bash

# Deploy script for Bay Area Camping Tracker
# This script updates the results and pushes to GitHub Pages

echo "🏕️ Bay Area Camping Tracker - Deploy Script"
echo "============================================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    echo "Please run this from your project directory"
    exit 1
fi

# Check if we have uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes"
    echo "Please commit or stash your changes before deploying"
    exit 1
fi

# Run the campsite search
echo "🔍 Running campsite search..."
python3 main.py

if [ $? -ne 0 ]; then
    echo "❌ Error: Campsite search failed"
    exit 1
fi

# Check if results.json was updated
if [ ! -f "results.json" ]; then
    echo "❌ Error: results.json not found"
    exit 1
fi

# Add and commit the updated results
echo "📝 Committing updated results..."
git add results.json
git commit -m "Update campsite search results - $(date '+%Y-%m-%d %H:%M')"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully deployed to GitHub Pages!"
    echo "🌐 Your site will be available at: https://mrsamlee.github.io/yayarea.camp/"
    echo "⏰ It may take a few minutes for the changes to appear"
else
    echo "❌ Error: Failed to push to GitHub"
    exit 1
fi
