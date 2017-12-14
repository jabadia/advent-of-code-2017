import json

import requests
from datetime import datetime
from pytz import timezone
from os import path
import dateutil.parser

from secrets import SESSION, LEADERBOARD

local_timezone = timezone('Europe/Madrid')

URI = 'http://adventofcode.com/{year}/day/{day}/input'
CACHE_DIR = './.cache'
DATE_FORMAT = '%m-%d %H:%M'


def get_leaderboard():
    now = datetime.now()
    key = "d{:02}-h{:02}{:02}.json".format(now.day, now.hour, (now.minute // 10) * 10)
    cached = path.join(CACHE_DIR, key)
    try:
        with open(cached) as f:
            return json.load(f)
    except (OSError, IOError) as err:
        print(err)
        response = requests.get(LEADERBOARD, cookies={'session': SESSION})
        response.encoding = 'utf-8'
        with open(cached, 'w') as f:
            f.write(response.text)
        return response.json()


if __name__ == '__main__':
    leaderboard = get_leaderboard()

    days = {}
    for member_id, member in leaderboard['members'].items():
        print(member['name'])
        for day, timestamps in sorted(member['completion_day_level'].items(), key=lambda p: int(p[0])):
            silver = dateutil.parser.parse(timestamps['1']['get_star_ts']).astimezone(local_timezone)
            gold = dateutil.parser.parse(timestamps['2']['get_star_ts']).astimezone(local_timezone)
            print(day, silver.strftime(DATE_FORMAT), gold.strftime(DATE_FORMAT), gold-silver)
