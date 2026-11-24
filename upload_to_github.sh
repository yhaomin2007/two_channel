#!/usr/bin/env bash
set -euo pipefail
# Usage: bash upload_to_github.sh
# Requires git, access to GitHub and credentials authorized to push.
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_url="https://github.com/yhaomin2007/two_channel.git"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
git clone "$repo_url" "$tmp/two_channel"
# Copy user files and generated output, preserving the established subdirectories.
cp -a "$script_dir"/. "$tmp/two_channel"/
cd "$tmp/two_channel"
git add -A
if git diff --cached --quiet; then echo 'No changes'; exit 0; fi
git commit -m 'Archive complete two-channel corrosion project files'
git push origin HEAD:main
echo "Uploaded to: $repo_url"
