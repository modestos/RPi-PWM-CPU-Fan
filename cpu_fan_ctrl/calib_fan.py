#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Interactive fan calibration helper.

Allows typing a duty-cycle value to apply to the fan. Validates input and
cleans up GPIO on exit.
"""

from typing import Any
import logging
import signal
import sys

import RPi.GPIO as GPIO

FAN_PIN = 21
PWM_FREQ = 25


def _signal_handler(signum: int, frame: Any) -> None:
    logging.info("Received signal %s, exiting", signum)
    sys.exit(0)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
    fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
    fan.start(0)

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    try:
        while True:
            try:
                val = input("Fan Speed (0-100): ")
            except EOFError:
                break
            val = val.strip()
            if not val:
                continue
            try:
                duty = float(val)
            except ValueError:
                logging.warning("Invalid number: %s", val)
                continue
            duty = max(0.0, min(100.0, duty))
            fan.ChangeDutyCycle(int(round(duty)))

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
    
