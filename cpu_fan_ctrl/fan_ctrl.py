#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple PWM fan controller for Raspberry Pi.

Improvements: structured entrypoint, logging, safe file I/O, signal handling
and GPIO cleanup on exit.
"""

from typing import List
import logging
import signal
import sys
import time

import RPi.GPIO as GPIO

# Configuration
FAN_PIN = 21  # BCM pin used to drive transistor's base
WAIT_TIME = 1  # [s] Time to wait between each refresh
FAN_MIN = 30  # [%] Fan minimum speed.
PWM_FREQ = 25  # [Hz]

# Configurable temperature and fan speed steps
tempSteps: List[float] = [30, 35, 40, 50, 60, 70]  # [°C]
speedSteps: List[float] = [0, 35, 40, 60, 80, 100]  # [%]

# Fan speed will change only if the difference of temperature is higher than hysteresis
hyst = 1.0


def read_cpu_temp() -> float:
    """Read CPU temperature from sysfs and return degrees Celsius."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return float(f.read().strip()) / 1000.0
    except FileNotFoundError:
        logging.error("Temperature sensor file not found")
        raise
    except Exception:
        logging.exception("Failed to read CPU temperature")
        raise


def interpolate(x: float, xs: List[float], ys: List[float]) -> float:
    """Linearly interpolate y for given x using step vectors xs and ys."""
    if x < xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]
    for i in range(len(xs) - 1):
        if xs[i] <= x < xs[i + 1]:
            # linear interpolation
            return (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]) * (x - xs[i]) + ys[i]
    return ys[-1]


running = True


def _signal_handler(signum, frame):
    global running
    logging.info("Received signal %s, shutting down", signum)
    running = False


def main() -> int:
    global running

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    if len(tempSteps) != len(speedSteps):
        logging.error("tempSteps and speedSteps must have same length")
        return 2

    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
    fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
    fan.start(0)

    cpuTempOld = 0.0
    fanSpeedOld = -1.0

    try:
        while running:
            try:
                cpuTemp = read_cpu_temp()
            except Exception:
                time.sleep(WAIT_TIME)
                continue

            if abs(cpuTemp - cpuTempOld) > hyst:
                fanSpeed = float(interpolate(cpuTemp, tempSteps, speedSteps))

                # Enforce minimum speed to prevent stalling
                if 0 < fanSpeed < FAN_MIN:
                    fanSpeed = FAN_MIN

                if fanSpeed != fanSpeedOld:
                    duty = int(round(fanSpeed))
                    logging.info("Setting fan duty cycle to %s%% (temp=%.1f°C)", duty, cpuTemp)
                    fan.ChangeDutyCycle(duty)
                    fanSpeedOld = fanSpeed
                cpuTempOld = cpuTemp

            time.sleep(WAIT_TIME)

    finally:
        logging.info("Cleaning up GPIO and exiting")
        try:
            fan.ChangeDutyCycle(0)
        except Exception:
            pass
        GPIO.cleanup()

    return 0


if __name__ == "__main__":
    sys.exit(main())
