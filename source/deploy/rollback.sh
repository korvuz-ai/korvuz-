#!/bin/sh
set -eu
backup=${1:?Usage: rollback.sh /opt/korvuz-backups/release-id}
case "$backup" in /opt/korvuz-backups/*) ;; *) exit 2 ;; esac
test -f "$backup/nginx.previous.conf"
install -o root -g root -m 644 "$backup/nginx.previous.conf" /etc/nginx/sites-available/korvuz.site.rollback-pending
mv -T /etc/nginx/sites-available/korvuz.site.rollback-pending /etc/nginx/sites-available/korvuz.site
nginx -t
systemctl reload nginx
