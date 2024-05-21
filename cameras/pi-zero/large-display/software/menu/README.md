### About

Below you can see the coordinate system

<img src="./menu-coordinate-system.png"/>

When entering a specific menu subpage/state, the coordinate system is with respect to the active sub menu.

### Menu map

<img src="./menu-map.png"/>

### Functional

- video recording (no time, no live passthrough)
- file counter (file view only does 1 page, images only)
- settings (only has raw telemetry sub-sub page)

### Not Functional

- battery indicator
- auto/manual camera mode eg. shutter/exposure settings

### Development notes

In order to add a new menu page/state wrt the buttons, edit these two files:

- display.py
- menu.py

See this [PR](https://github.com/jdc-cunningham/modular-pi-cam/pull/13/files) for an example adding battery reset
