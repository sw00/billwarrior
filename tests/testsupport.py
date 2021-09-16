from datetime import datetime, timedelta
from random import randint

from timewreport.interval import TimeWarriorInterval

DT_FORMAT = "%Y%m%dT%H%M%SZ"


def give_interval(day=None, tags=[]):
    if day:
        start = day.replace(hour=randint(0, 12))
    else:
        start = datetime.today().replace(day=randint(1, 28), month=randint(1, 12))

    end = start + timedelta(0, randint(60 * 5, 60 * 60 * 2))  # up to 2h

    return TimeWarriorInterval(start.strftime(DT_FORMAT), end.strftime(DT_FORMAT), tags)
