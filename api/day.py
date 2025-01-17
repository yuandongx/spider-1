from datetime import datetime
import calendar
from .app import app

weekday_name = ("一", "二", "三", "四", "五", "六", "日")

@app.get("/today")
async  def today():
    now = datetime.now()
    return {
        "statusCode": 200,
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "second": now.second,
        "weekday": now.weekday(),
        "weekday_name": weekday_name[now.weekday()],
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/month/{year}/{month}")
async def get_month(year:int, month:int):
    """the weekdays of `month` """
    cal = calendar.Calendar()
    _days = []
    for day, weekday in cal.itermonthdays2(year, month):
        if 0 < day < 32:
            _days.append({"day": day, "weekday": weekday_name[weekday]})
    return {
        "statusCode": 200,
        "days": _days
    }