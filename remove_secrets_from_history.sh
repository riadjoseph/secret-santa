#!/bin/bash

# This script removes .env.example from git history
# WARNING: This rewrites git history. Only run if you haven't shared this repo with others.

echo "⚠️  WARNING: This will rewrite git history!"
echo "This will remove .env.example from all commits."
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "Removing .env.example from git history..."

# Use git filter-branch to remove the file from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env.example" \
  --prune-empty --tag-name-filter cat -- --all

echo ""
echo "✅ .env.example removed from git history"
echo ""
echo "Next steps:"
echo "1. Force push to GitHub: git push origin --force --all"
echo "2. IMMEDIATELY rotate your Supabase keys in the Supabase dashboard"
echo "3. Update .env and .streamlit/secrets.toml with new keys"
