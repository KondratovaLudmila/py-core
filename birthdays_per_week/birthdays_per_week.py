from datetime import datetime, timedelta, date
from collections import defaultdict

TEST_USERS = [
                {"name": "Bill",
                 "birthday": datetime(year=1956, month=8, day=17).date()},
                 {"name": "Jill",
                 "birthday": datetime(year=1976, month=9, day=4).date()},
                 {"name": "Pol",
                 "birthday": datetime(year=1958, month=9, day=8).date()},
                 {"name": "Rob",
                 "birthday": datetime(year=1999, month=9, day=11).date()},
                 {"name": "Anna",
                 "birthday": datetime(year=1985, month=9, day=14).date()},
                 {"name": "Kate",
                 "birthday": datetime(year=1985, month=9, day=13).date()}]

PERIOD = timedelta(days=7)

WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thurthday", "Friday"]

def actual_birthday(birthday: date, start: date) -> date:

    if start <= birthday.replace(year=start.year):
        return birthday.replace(year=start.year)
    else:
        return birthday.replace(year=start.year + 1)
    
def  get_birthdays_per_week(users: dict) -> dict:
    
    if not users:
        return {}

    birthdays = defaultdict(list)
    cur_date = date.today()
    cur_weekday = cur_date.weekday()
    
    if cur_weekday == 0:
        cur_date -= timedelta(days=2)
    end_date = cur_date + PERIOD

    for user in users:
        cur_birthday = actual_birthday(user["birthday"], cur_date)
        
        if cur_date <= cur_birthday < end_date:
            weekday = cur_birthday.weekday()
            if weekday >= len(WEEK_DAYS):
                weekday = 0
            
            birthdays[WEEK_DAYS[weekday]].append(user["name"])

    return birthdays

def print_birthdays(birthdays: list):
    cur_weekday = date.today().weekday()
    week_len = len(WEEK_DAYS)
    for idx in range(cur_weekday, cur_weekday + week_len):
        weekday = WEEK_DAYS[idx % week_len]
        if birthdays[weekday] == []:
            continue
        print(f"{weekday}: {', '.join(birthdays[weekday])}")

if __name__ == "__main__":
    
    birthday_list = get_birthdays_per_week(TEST_USERS)
    print_birthdays(birthday_list)