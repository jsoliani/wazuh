#!/bin/bash

if [ $1 ]; then
  if [ ! -f "$1" ]; then
    echo "Error: File not found!"
    exit 1
  fi
else
  echo -e "Error: Parameter missing!\n       Usage: eps-counter.sh <filename>"
  exit 1
fi

run_for_secs=21600 # 21600 segundos son 6 horas, 43200 = 12 horas, 86400 = 24 horas
logFile="/var/ossec/logs/eps-counter.log"
lines_now=$(wc -l < "$1")
lines_added_total=0
seconds=0
interval=60
loop_cycles=$[$run_for_secs/$interval]

echo "[INFO] - $(date +%Y-%m-%dT%H:%M:%S) - EPS Counter started (found $lines_now lines in $1, interval=${interval}s, will run for=${run_for_secs}s)" >> $logFile
sleep $interval

for ((i=1; i<=$loop_cycles; i++)); do
    seconds=$[$seconds + $interval]
    lines_added=$(head -n -$lines_now "$1" | wc -l)
    if [ "$lines_added" -gt 0 ]; then
        lines_added_total=$[$lines_added + $lines_added_total]
        lines_now=$[ $lines_now + $lines_added ]
    fi
    if [ $(($seconds % $interval)) -eq 0 ]; then echo -e "[INFO] - $(date +%Y-%m-%dT%H:%M:%S) - STATS = $lines_added_total added, $lines_now total, $seconds seconds passed, EPS: $(echo 3k $lines_added_total $seconds /p | dc)" >> $logFile
    fi
    sleep $interval
done
