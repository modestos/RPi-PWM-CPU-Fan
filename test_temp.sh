#!/usr/bin/env bash
# script to test RPi 4 temperature
# installation requirements include: sudo apt-get install sysbench

set -euo pipefail

clear

if ! command -v vcgencmd >/dev/null 2>&1; then
        echo "vcgencmd not found in PATH. Install libraspberrypi-bin or run on a Pi." >&2
        exit 2
fi
if ! command -v sysbench >/dev/null 2>&1; then
        echo "sysbench not found in PATH. Install sysbench to run the CPU test." >&2
        exit 2
fi

ITERATIONS=${1:-8}
PRIME=${2:-25000}
THREADS=${3:-4}

for ((i = 1; i <= ITERATIONS; i++)); do
        vcgencmd measure_temp
        sysbench --test=cpu --cpu-max-prime="$PRIME" --num-threads="$THREADS" run >/dev/null 2>&1
done

# measure cpu temp after test
vcgencmd measure_temp

