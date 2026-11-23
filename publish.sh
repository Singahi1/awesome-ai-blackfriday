#!/usr/bin/env bash
# Publish this folder to GitHub Pages. One-time, after `gh auth login`.
#   ./publish.sh [repo-name]
set -euo pipefail
REPO="${1:-awesome-ai-blackfriday}"
OWNER="$(gh api user -q .login)"
cd "$(dirname "$0")"

python3 scripts/validate.py
python3 scripts/build_readme.py

git init -q 2>/dev/null || true
git add -A
git commit -q -m "deals: refresh $(date +%F)" || true

# create the repo only if it doesn't exist yet
if ! gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  gh repo create "$REPO" --public --source . --remote origin --push \
    --description "Curated, sourced Black Friday deals on AI tools — with the price before, after and at renewal."
else
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$OWNER/$REPO.git"
  git push -u origin main
fi

# serve from the repo root on main
gh api "repos/$OWNER/$REPO/pages" -X POST -f 'source[branch]=main' -f 'source[path]=/' 2>/dev/null \
  || gh api "repos/$OWNER/$REPO/pages" -X PUT  -f 'source[branch]=main' -f 'source[path]=/' >/dev/null

echo "→ https://$OWNER.github.io/$REPO/   (first build takes 1–3 min)"

# point the README header at the live URL
GH_OWNER="$OWNER" GH_REPO="$REPO" python3 scripts/build_readme.py
git add README.md && git commit -q -m "readme: link the live site" && git push -q
