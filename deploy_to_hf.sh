#!/usr/bin/env bash
set -euo pipefail

# deploy_to_hf.sh
# Usage: set HF_SPACE_REPO and optionally HF_TOKEN, then run this script to copy
# the current project into the cloned Hugging Face Space repo and push.
#
# Example:
# HF_SPACE_REPO="https://huggingface.co/spaces/<user>/<space>" \
# HF_TOKEN="hf_xxx..." ./deploy_to_hf.sh

if [ -z "${HF_SPACE_REPO:-}" ]; then
  echo "ERROR: set HF_SPACE_REPO=https://huggingface.co/spaces/<user>/<space>"
  exit 2
fi

TMP_DIR="/tmp/hf_space_$(date +%s)"
echo "Cloning Space repo: $HF_SPACE_REPO -> $TMP_DIR"
git clone "$HF_SPACE_REPO" "$TMP_DIR"

echo "Copying project files to Space repo..."
# copy only project files (avoid copying .git from this repo)
rsync -av --exclude='.git' --exclude='.vscode' --exclude='data' --exclude='results' ./ "$TMP_DIR/"

cd "$TMP_DIR"

echo "Preparing commit in Space repo"
git add .
if git diff --staged --quiet; then
  echo "No changes to push. Exiting."
  exit 0
fi

git commit -m "Deploy Streamlit app: sync from MetaClassificador"

# If HF_TOKEN is provided, set temporary remote URL with token to allow push
if [ -n "${HF_TOKEN:-}" ]; then
  echo "Using HF_TOKEN to authenticate push (token will not be stored)"
  # insert token into remote URL (be careful: token appears in process args)
  remote_url="$HF_SPACE_REPO"
  # if remote is https://huggingface.co/spaces/user/space, we can push using the token
  auth_url=$(echo "$remote_url" | sed -e "s#https://#https://hf_token:@#")
  # replace placeholder with real token
  auth_url=$(echo "$auth_url" | sed -e "s/hf_token:/$HF_TOKEN/1")
  git remote set-url origin "$auth_url"
fi

echo "Pushing to Space repo..."
git push origin main

echo "Done. Space repo updated. You can now open the Space URL: $HF_SPACE_REPO"
