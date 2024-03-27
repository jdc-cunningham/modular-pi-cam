### Physical measurements

- camera booting 220mA
- idling 170mA
- active ssh 200mA
- solid white OLED 350mA
- live camera passthrough, OLED painting full speed, 560mA

### Thoughts on software battery tracking

The battery I'm using is a single cell 720mA, it's not a lot

There is no hardware to detect battery level. The charger has a low-voltage cut off... but trying to avoid that.

Best case scenario 3hrs based on 200mA idling, not 100% usage

When the camera enters a high-current draw state like live camera pass through, this should be logged somewhere which would factor into the soft battery limit (CRON/database/OLED warning).

I don't know how yet to merge this info together to have something that self-corrects.

- on boot ask if battery charged yes/no
- CRON job every 5 minutes store into sqlite db
- high-power usage duration logged
- combine the figures above against 3hrs and use that as battery level
