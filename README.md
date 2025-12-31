# RPi PWM CPU Fan Controller

Lightweight Raspberry Pi PWM CPU fan controller. Reads CPU temperature and controls a PWM fan via GPIO using the Python scripts in `cpu_fan_ctrl/`.

## Contents

- `display_temp.sh` - simple temperature display helper script
- `test_temp.sh` - simple test script for temperature reading
- `cpu_fan_ctrl/`
  - `calib_fan.py` - fan calibration helper
  - `fan_ctrl.py` - main fan control program
  - `fanctrl.service` - example systemd service unit

## Requirements

- Raspberry Pi with a PWM-capable GPIO pin connected to the fan controller
- Python 3.7+ (Python 3.11 recommended)
- `pip` for installing any optional Python dependencies
- Optionally `pigpio` or `RPi.GPIO` depending on how `fan_ctrl.py` is configured

## Installation

1. Clone the repository:

   git clone <your-repo-url>
   cd "RPi PWM CPU Fan"

2. (Optional) Create and activate a virtual environment:

   python3 -m venv .venv
   source .venv/bin/activate

3. Install any needed Python packages (if required by your chosen GPIO library):

   pip install pigpio RPi.GPIO

4. Configure `fan_ctrl.py` if necessary (GPIO pin, PWM settings).

## Usage

- Display current temperature:

  ./display_temp.sh

- Run a quick temperature test:

  ./test_temp.sh

- Run the fan controller manually:

  python3 cpu_fan_ctrl/fan_ctrl.py

- Calibrate the fan curve and PWM behavior:

  python3 cpu_fan_ctrl/calib_fan.py


## Systemd Service (optional)

Recommended service configuration: set `WorkingDirectory` to the repository path on the target
Pi so the service can run the relative `ExecStart` path. Replace `/path/to/repo` with the
absolute path on your Raspberry Pi (for example `/home/pi/temperature_management`).

Example unit file contents (recommended):

```
[Unit]
Description=PWM Fan Control
After=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/path/to/repo
ExecStart=/usr/bin/env python3 -u cpu_fan_ctrl/fan_ctrl.py
Restart=on-failure
RestartSec=5
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Install and enable the service (replace `/path/to/repo` accordingly):

```
sudo cp cpu_fan_ctrl/fanctrl.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now fanctrl.service
sudo systemctl status fanctrl.service
journalctl -u fanctrl.service -f
```

Notes:

- Use a non-root user (e.g., `pi`) where possible; grant that user GPIO access (via groups
  or running with `pigpio` socket) instead of running as `root` when practical.
- If you prefer not to set `WorkingDirectory`, change `ExecStart` to an absolute script path.
- The included `cpu_fan_ctrl/fanctrl.service` in the repo is a starting point — update it to
  include the correct `WorkingDirectory` or absolute `ExecStart` before installing.

## Configuration

Edit `cpu_fan_ctrl/fan_ctrl.py` to adjust:

- GPIO pin assignment
- Temperature-to-PWM mapping / control curve
- Logging verbosity

## Troubleshooting

- If PWM output doesn't behave as expected, confirm wiring and that the chosen GPIO supports PWM.
- If the service fails to start, inspect `journalctl -u fanctrl.service` for errors.

## License

This repository is provided as-is. Add a license file if you want to declare explicit terms.

## Contact

For questions or improvements, open an issue or submit a pull request.
