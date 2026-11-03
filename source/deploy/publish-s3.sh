#!/usr/bin/env bash
# Usage: publish-s3.sh <site_dir>   (e.g. a release dir containing index.html)
set -euo pipefail
SRC="${1:?site dir}"; B=korvuz-site-web; REG=ap-southeast-7; DIST=ED0OZJJZJXJ8R
[ -f "$SRC/index.html" ] || { echo "no index.html in $SRC"; exit 1; }
aws s3 sync "$SRC" "s3://$B" --delete --exclude 'release-manifest.json' --exclude 'assets/media/*' --cache-control 'no-cache' --region $REG --only-show-errors
[ -d "$SRC/assets/media" ] && aws s3 sync "$SRC/assets/media" "s3://$B/assets/media" --delete --cache-control 'public, max-age=31536000, immutable' --region $REG --only-show-errors
aws cloudfront create-invalidation --distribution-id $DIST --paths '/*' --query Invalidation.Id --output text
