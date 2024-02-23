### Deps
* need SPI enabled (raspi-config)

### Boot script

There is a boot script that runs `main.py` in the `software` folder

It uses systemd, see the basic service file below below (systemd service)

Create a file named `modular-pi-cam.service` in the `/etc/systemd/system/` folder

```
[Unit]
Description=Start Modular Pi Cam
After=multi-user.target

[Service]
Type=idle
WorkingDirectory=/home/pi/modular-pi-cam/camera/pi-zero/software
User=pi
ExecStart=/usr/bin/python3 /home/pi/modular-pi-cam/camera/pi-zero/software/main.py
Restart=no

[Install]
WantedBy=multi-user.target
```

Add the service

```
$sudo nano /etc/systemd/system/modular-pi-cam.service
$sudo systemctl enable modular-pi-cam.service
$sudo systemctl daemon-reload
$sudo systemctl restart modular-pi-cam.service
```

Verify it's working with

`$sudo systemctl status modular-pi-cam.service`

### Development notes

As of this time I have not found a way to mount/develop against the Pi. I also have not mocked the features eg. the menu/display render (maybe a simulator).

I am using SFTP to edit files on the pi and then run the code via ssh session

### Battery profiling

`*/5 * * * * /usr/bin/python /home/pi/modular-pi-cam/camera/software/cron.py >> /home/pi/modular-pi-cam-cron.log 2>&1`

Verify python binary location via `$which python`

There is a Sqlite database `battery.db` that keeps track of the camera's uptime and a CRON job that increments a DB entry every 5 minutes.

In the settings menu there is a `battery profiler` function which you would run after fully charging your pi cam.

There is not an accurate estimate of usage based on idle and dynamic current draw (highest being camera on, live preview on display)
