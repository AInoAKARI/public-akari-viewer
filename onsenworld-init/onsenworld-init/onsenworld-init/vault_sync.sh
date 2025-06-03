#!/usr/bin/env bash
# vault_sync.sh
# Sync latest .json and .mp3 files to Vault path

set -e

SRC_DIR=${1:-"."}
DATE_DIR=$(date +"%Y%m%d_%H%M%S")
DEST="/akarihearts-v2/data/onsenworld/${DATE_DIR}"

echo "Syncing to $DEST"

# Example using rclone (uncomment and configure remote "vault")
# rclone copy "$SRC_DIR" "vault:$DEST" --include "*.json" --include "*.mp3"

# Placeholder using rsync to local path (for local testing)
mkdir -p "$DEST"
rsync -av --include="*/" --include="*.json" --include="*.mp3" --exclude="*" "$SRC_DIR/" "$DEST/"

echo "Done."
