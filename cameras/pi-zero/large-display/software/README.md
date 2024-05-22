### Deps

- need SPI enabled (raspi-config)

### Boot script (ROOT)

Disclaimer: you can disable root user here by not having USB or dealing with non-sudo user usb mount support

There is a boot script that runs `main.py` in the `software` folder

It uses systemd, see the basic service file below below (systemd service)

Create a file named `pi-cam.service` in the `/etc/systemd/system/` folder

```
[Unit]
Description=Start Modular Pi Cam
After=multi-user.target

[Service]
Type=idle
WorkingDirectory=/home/pi/modular-pi-cam/cameras/pi-zero/large-display/software
User=root
ExecStart=/usr/bin/python3 /home/pi/modular-pi-cam/cameras/pi-zero/large-display/software/main.py
Restart=always

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

As of this time I have not found a way to mount/develop against the Pi. I also have not mocked the features eg. OLED, etc... to run on say a Windows computer.

I am using SFTP to edit files on the pi and then run the code via ssh session

#### Microphone support

You will need to install `pyaudio` on bookworm that's done with `sudo apt install python3-pyaudio`

The microphone is also currently hardcoded/assumed so check the name that your device appears as with `test-usb-mic-recording.py` and put that in or the first non-default option is assumed

#### USB support (running as root)

In order to do auto mounting of a flash drive you have to be root using `/mnt` and the `mount` command.

The `modular-pi-cam.service` above is set to be root user

Alternative is to use something like `udisk2` or `udiskctl`

`udisk2` should already be available or added by `sudo apt install udisks2`

`udiskctl` also requires sudo unless some [permissions are not met]('https://unix.stackexchange.com/a/738504/133821')...

This service will run as root for now

#### Mic dislcaimer:

The USB mic in my case would turn the pi zero 2 off when plugging it in... so the mic should be plugged in BEFORE starting the pi

### Battery profiling

`*/5 * * * * /usr/bin/python /home/pi/modular-pi-cam/cameras/pi-zero/large-display/software/cron_battery_ticker.py >> /home/pi/cron-battery-ticker.log 2>&1`

Verify python binary location via `$which python`

There is a Sqlite database `battery.db` that keeps track of the camera's uptime and a CRON job that increments a DB entry every 5 minutes.

In the settings menu there is a `battery profiler` function which you would run after fully charging your pi cam.

It is a loose estimate since it does not reflect how many times the user has turned the live preview on/off... it's about 75% of max capacity... based 50% testing eg. 50% preview on/off before camera dies + 25% of that to be under 80% battery usage.

I had measured some current draw values before based on what the camera is doing but I did not do a good job/accurately do it, plus the electronics changed since then. But the highest current draw is during live camera preview eg. around 600mA. For reference the pi zero 1 would draw around 65mA during idle.
