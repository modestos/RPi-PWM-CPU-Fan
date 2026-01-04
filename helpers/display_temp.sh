#!/usr/bin/env bash
# script to test RPi 4 temperature
# installation requirements include: sudo apt-get install sysbench

set -euo pipefail

clear

timestamp() {
	date +"%F %T"
}

if ! command -v vcgencmd >/dev/null 2>&1; then
	echo "vcgencmd not found in PATH. Install libraspberrypi-bin or run on a Pi." >&2
	exit 2
fi

echo "This script displays the current CPU temperature."
read -r -p "Input number of iterations (e.g. 10): " iterations
if ! [[ $iterations =~ ^[0-9]+$ ]]; then
	echo "Invalid iteration count" >&2
	exit 2
fi

read -r -p "Input sleep interval in seconds (e.g. 20): " timeinterval
if ! [[ $timeinterval =~ ^[0-9]+$ ]]; then
	echo "Invalid time interval" >&2
	exit 2
fi

for ((c=1; c<=iterations; c++)); do
	echo "$(timestamp): $(vcgencmd measure_temp)"
	sleep "$timeinterval"
done

echo "all Done."


