#!/bin/bash
# Restore workspace from GitHub backup
# WARNING: This will overwrite local changes

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh [remote_url]"
    echo "Example: ./restore.sh https://github.com/YOUR_USERNAME/two-backup.git"
    exit 1
fi

echo "⚠️  WARNING: This will overwrite local changes!"
read -p "Continue? (y/N) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Reset to clean state
git fetch origin
git reset --hard origin/master
git clean -fd

# Restore config files from backup
if [ -f /root/.openclaw/workspace/config-backup/openclaw.json ]; then
    cp /root/.openclaw/workspace/config-backup/openclaw.json /root/.openclaw/openclaw.json
    echo "✓ Config restored"
fi

echo "✓ Workspace restored from GitHub backup"
echo "  Restart OpenClaw gateway: systemctl --user restart openclaw-gateway"
