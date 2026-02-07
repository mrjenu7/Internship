import calendar

c = calendar.TextCalendar(calendar.MONDAY)
thestr = c.formatmonth(2026, 1)
print(thestr)

hc = calendar.HTMLCalendar(calendar.MONDAY)
thestrg = hc.formatmonth(2026, 1)
print(thestrg)


#iterate month and weeks:

import calendar

c = calendar.TextCalendar(calendar.MONDAY)

for i in c.itermonthdays(2026, 8):
    print(i)

for name in calendar.month_name:
    print(name)

for day in calendar.day_name:
    print(day)


#print first friday of all months:

print("Team meetings will be on:")

for m in range(1, 13):
    cal = calendar.monthcalendar(2026,m)
    weekone = cal[0]
    weektwo = cal[1]

    if weekone[calendar.FRIDAY]!=0:
        meetday = weekone[calendar.FRIDAY]
    else:
        meetday = weektwo[calendar.FRIDAY]

    print(f"{calendar.month_name[m]}: {meetday}")