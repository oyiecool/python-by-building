# Disk full on a web server
Symptoms: uploads fail, "No space left on device" in nginx or app logs, slow responses.
1. Check usage with df -h and find big directories with du -xh / | sort -h | tail.
2. Rotate or compress old logs in /var/log (logrotate -f /etc/logrotate.conf).
3. Clear the app's tmp upload folder of files older than 2 days.
4. Restarting nginx does NOT free space; only do it after space is back if errors continue.
