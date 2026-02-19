#!/bin/bash
# Backup workspace to GitHub
# Run this regularly or set up a cron job

REPO="${REPO:-two-backup}"
MESSAGE="${1:-Auto-backup $(date +%Y-%m-%d\ %H:%M)}"

# Backup key config files (they live outside workspace)
mkdir -p /root/.openclaw/workspace/config-backup
cp /root/.openclaw/openclaw.json /root/.openclaw/workspace/config-backup/

# Add all changes
git add -A

# Check if there are changes
if git diff --staged --quiet; then
    echo "No changes to commit. Backup up to date."
    exit 0
fi

# Commit
git commit -m "$MESSAGE"

# Push to GitHub
git push origin master
echo "✓ Backup pushed to GitHub"
