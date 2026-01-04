#!/usr/bin/env python3
"""Simple smoke test for the fan controller module.

This test verifies the module imports and the interpolation helper.
"""
import sys

try:
    from cpu_fan_ctrl import fan_ctrl
except Exception as e:
    print("Failed to import cpu_fan_ctrl.fan_ctrl:", e)
    sys.exit(2)


def test_interpolate():
    # simple check: interpolate between 30->0 and 40->100 at x=35 -> 50
    x = 35.0
    xs = [30.0, 40.0]
    ys = [0.0, 100.0]
    val = fan_ctrl.interpolate(x, xs, ys)
    assert round(val, 1) == 50.0, f"unexpected interpolate result: {val}"


def main():
    test_interpolate()
    print("smoke_test: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
