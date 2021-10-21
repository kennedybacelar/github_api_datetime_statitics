from typing import List, Dict
from pprint import pprint
from datetime import date, datetime, timedelta, timezone
from dataclasses import dataclass
from enum import Enum


class Interval(str, Enum):
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"


CHALLENGE_PART_1 = """

    Let's implement the `calculate_datetimes_between` function, with the following rules:

    In all cases all datetimes must be smaller than end of the day of `to_date`

    If `interval == Interval.month`
      return with the starting of the months (1st day of the month, 00:00:00 time)
      starting from the 1st of the month of `from_date`

    If `interval == Interval.week`
      return all Mondays with time 00:00:00 starting from the week of `from_date`

    If `interval == Interval.day`
      return all days with time 00:00:00 starting from `from_date`

    if `interval == Interval.hour`
      return all hours with 0 minutes 0 seconds starting from `from_date` 00:00:00

"""

CHALLENGE_PART_2 = """

    Create a small HTTP API where users can get a simple statistics on Repository Pull Requests.
    We are interested in the number of pull requets created in the GitHub repository.

    If I want to know the number of pull requets created every day in the
        * repository github.com/kubernetes/kubernetes
        * between 2021-01-01 and 2021-03-31
        * grouped by days

    I can send the following request:

    {
        "from_date": "2021-01-01",
        "to_date": "2021-03-31",
        "interval": "day",
        "repository": "kubernetes/kubernetes"
    }

    I should get a reponse with a list of objects where every object has a "timestamp" and a "count" key.

    [
        {"timestamp": "2021-01-01T00:00:00", "count": 10},
        {"timestamp": "2021-01-02T00:00:00", "count": 5},
        {"timestamp": "2021-01-03T00:00:00", "count": 6},
        ...
    ]

    Additional Requirements:
        * Interval can be hour/day/week/month
        * Use FastAPI for the implementation! (https://fastapi.tiangolo.com/)
        * Handle errors where the repository doesn't exists, or the GitHub API returns with other than 200.


    Hints:
        * Use the calculate_datetimes_between function to get all the timestamps needed for the response.
        * USe GitHub API to get the list of Pull Requests. Example https://api.github.com/repos/kubernetes/kubernetes/pulls
        * Depending on the time interval you may need multiple requets to get all the pull requets.
        * To avoid GitHub API rate limit, you can register a Personal Access Token
        (https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)


"""


def calculate_datetimes_between(from_date: date, to_date: date, interval: Interval) -> List[datetime]:
    
    response = []
    from_date = datetime(from_date.year, from_date.month, from_date.day, 0, 0, tzinfo=timezone.utc)
    to_date = datetime(to_date.year, to_date.month, to_date.day, 0, 0, tzinfo=timezone.utc)
    
    if interval == interval.month:
      while(True):
        if from_date > to_date:
          break
        from_date = datetime(from_date.year, from_date.month, 1, 0, 0, tzinfo=timezone.utc)
        response.append(from_date)
        
        if from_date.month == 2:
          from_date = from_date + timedelta(days=28)
        else:
          from_date = from_date + timedelta(days=31)
    
    if interval == interval.week:
      first = True
      while(True):
        if from_date > to_date:
          break
        while(first):
          if from_date.weekday() == 0:
            first = False
            break
          from_date = from_date - timedelta(days=1)
        response.append(from_date)
        from_date = from_date + timedelta(days=7)
    
    if interval == interval.day:
      while(True):
        if from_date > to_date:
          break
        from_date = datetime(from_date.year, from_date.month, from_date.day, 0, 0, tzinfo=timezone.utc)
        response.append(from_date)
        from_date = from_date + timedelta(days=1)
    
    if interval == interval.hour:
      while(True):
        if from_date.date() > to_date.date():
          break
        from_date = datetime(from_date.year, from_date.month, from_date.day, from_date.hour, 0, tzinfo=timezone.utc)
        response.append(from_date)
        from_date = from_date + timedelta(hours=1)

    return response


"""
Example cases for testing
"""


@dataclass
class Example:
    from_date: date
    to_date: date
    interval: Interval
    result: List[datetime]


EXAMPLES: Dict[str, Example] = {
    "empty_hour_interval": Example(date(2021, 5, 20), date(2021, 5, 19), Interval.hour, []),
    "single_day_all_hours": Example(
        date(2021, 5, 20),
        date(2021, 5, 20),
        Interval.hour,
        [
            datetime(2021, 5, 20, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 1, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 2, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 3, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 4, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 5, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 6, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 7, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 8, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 9, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 10, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 11, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 12, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 13, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 14, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 15, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 16, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 17, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 18, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 19, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 20, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 21, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 22, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 23, 0, tzinfo=timezone.utc),
        ],
    ),
    "single_week_all_days": Example(
        date(2021, 5, 17),
        date(2021, 5, 23),
        Interval.day,
        [
            datetime(2021, 5, 17, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 18, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 19, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 20, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 21, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 22, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 23, 0, 0, tzinfo=timezone.utc),
        ],
    ),
    "all_week_start_related_to_may": Example(
        date(2021, 5, 1),
        date(2021, 5, 31),
        Interval.week,
        [
            datetime(2021, 4, 26, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 3, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 10, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 17, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 24, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 31, 0, 0, tzinfo=timezone.utc),
        ],
    ),
    "all_months_for_a_year": Example(
        date(2021, 1, 1),
        date(2021, 12, 31),
        Interval.month,
        [
            datetime(2021, 1, 1, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 2, 1, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 3, 1, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 4, 1, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 5, 1, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 6, 1, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 7, 1, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 8, 1, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 9, 1, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 10, 1, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 11, 1, 0, 0, tzinfo=timezone.utc),
            datetime(2021, 12, 1, 0, 0, tzinfo=timezone.utc),
        ],
    ),
    "tricky_month_start": Example(
        date(2021, 2, 28),
        date(2021, 3, 1),
        Interval.month,
        [datetime(2021, 2, 1, 0, 0, tzinfo=timezone.utc), datetime(2021, 3, 1, 0, 0, tzinfo=timezone.utc)],
    ),
    "tricky_week_start": Example(
        date(2021, 2, 28),
        date(2021, 3, 1),
        Interval.week,
        [datetime(2021, 2, 22, 0, 0, tzinfo=timezone.utc), datetime(2021, 3, 1, 0, 0, tzinfo=timezone.utc)],
    ),
    "tricky_day": Example(
        date(2021, 2, 28),
        date(2021, 3, 1),
        Interval.day,
        [datetime(2021, 2, 28, 0, 0, tzinfo=timezone.utc), datetime(2021, 3, 1, 0, 0, tzinfo=timezone.utc)],
    ),
}

if __name__ == "__main__":
    for name, example in EXAMPLES.items():
        try:
            assert calculate_datetimes_between(example.from_date, example.to_date, example.interval) == example.result
            print(f"Case {name} PASSED.")
        except AssertionError:
            print(f"Failed case: {name}")
            print("Expected:")
            pprint(example.result)
            print("Calculated:")
            pprint(calculate_datetimes_between(example.from_date, example.to_date, example.interval))
            print("-" * 80)
