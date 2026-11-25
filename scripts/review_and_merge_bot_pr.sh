#!/usr/bin/env bash
set -euo pipefail
PR="${1:?pull request number required}"
SUMMARY="${2:-bot-output/summary.json}"
REPO="${GITHUB_REPOSITORY:-Singahi1/awesome-ai-blackfriday}"

verification_only=$(jq -r '.verification_only' "$SUMMARY")
if [[ "$verification_only" == "true" ]]; then
  gh pr edit "$PR" --repo "$REPO" --add-label "safe-auto-merge" --remove-label "needs-human-review" || true
  gh pr comment "$PR" --repo "$REPO" --body "Automated review: verification metadata only (last-verified, next-check, verification state, evidence). No price, discount, deadline, lifecycle or sponsor term was changed. Dataset validation, static generation and smoke tests passed in the deal-bot job; squash-merging now." || true
  gh pr merge "$PR" --repo "$REPO" --squash --delete-branch
else
  gh pr edit "$PR" --repo "$REPO" --add-label "needs-human-review" --remove-label "safe-auto-merge" || true
  gh pr comment "$PR" --repo "$REPO" --body "Automated review: this PR contains content changes (new offer, lifecycle change, or other non-metadata edit). It will not merge automatically. Review the evidence and generated diff before merging." || true
fi
