"""
Break a 24 hour day into 15 minute chunks. There are 96 of them.
The sets below represent the intervals that represent that schedule

For example EVERY_SIX_HOURS would look like {0, 24, 48, 72} and means that
something running on this schedule should run on intevals 0, 24, 48 and 72.

"""

NINETY_SIX = set(range(96))
DAILY = {item for item in NINETY_SIX if item % 96 == 0}
EVERY_TWELVE_HOURS = {item for item in NINETY_SIX if item % 48 == 0}
EVERY_SIX_HOURS = {item for item in NINETY_SIX if item % 24 == 0}
EVERY_FOUR_HOURS = {item for item in NINETY_SIX if item % 16 == 0}
EVERY_THREE_HOURS = {item for item in NINETY_SIX if item % 12 == 0}
EVERY_TWO_HOURS = {item for item in NINETY_SIX if item % 8 == 0}
HOURLY = {item for item in NINETY_SIX if item % 4 == 0}
HALF_HOURLY = {item for item in NINETY_SIX if item % 2 == 0}
EVERY_FIFTEEN_MINUTES = NINETY_SIX
