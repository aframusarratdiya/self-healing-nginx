#!/bin/sh
set -u
LOGFILE=/logs/access.log
echo "[collector] tailing ${LOGFILE}"
touch "${LOGFILE}"
while true; do
 echo "=== live traffic (last 15 requests) ==="
 tail -n 15 "${LOGFILE}" 2>/dev/null || true
 echo
 sleep 3
done
