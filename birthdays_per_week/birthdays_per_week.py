from datetime import datetime, timedelta
from collections import defaultdict

TEST_USERS = [
                {"name": "Bill",
                 "birthday": datetime(year=1956, month=8, day=17)},
                 {"name": "Jill",
                 "birthday": datetime(year=1976, month=8, day=11)},
                 {"name": "Pol",
                 "birthday": datetime(year=1958, month=8, day=19)},
                 {"name": "Rob",
                 "birthday": datetime(year=1999, month=8, day=18)},
                 {"name": "Anna",
                 "birthday": datetime(year=1985, month=8, day=14)},
                 {"name": "Kate",
                 "birthday": datetime(year=1985, month=8, day=13)}]

PERIOD = timedelta(days=7)

WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thurthday", "Friday"]

def  get_birthdays_per_week(users: dict) -> dict:
    
    if not users:
        return

    birthdays = defaultdict(list)
    cur_date = datetime.now()
    cur_weekday = cur_date.weekday()
    
    if cur_weekday == 0:
        cur_date -= timedelta(days=2)
    cur_date = datetime(year=cur_date.year, month=cur_date.month, day=cur_date.day)

    for user in users:
        actual_birthday = user["birthday"].replace(year=cur_date.year)
        if actual_birthday >= cur_date and actual_birthday < cur_date + PERIOD:
            weekday = datetime(year=actual_birthday.year, \
                               month=actual_birthday.month, \
                                day=actual_birthday.day).weekday()
            if weekday >= len(WEEK_DAYS):
                weekday = 0
            
            birthdays[WEEK_DAYS[weekday]].append(user["name"])

    week_len = len(WEEK_DAYS)
    for idx in range(cur_weekday, cur_weekday + week_len):
        weekday = WEEK_DAYS[idx % week_len]
        if birthdays[weekday] == []:
            continue
        print(f"{weekday}: {', '.join(birthdays[weekday])}")


if __name__ == "__main__":
    
    get_birthdays_per_week(TEST_USERS)