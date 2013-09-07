from calendar import Calendar
from datetime import date,timedelta

__author__ = 'Frostbite'
start = date(2013, 5, 11)
end = date(2013, 7, 20)
new = start + timedelta(days=150)
print end - start
print new.weekday()