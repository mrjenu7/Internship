#from datetime import date
from datetime import datetime

now = datetime.now()
print("current date and time is: ", now)

# Formating Time :

#print(now.strftime("%a %d %B %y"))
#print(now.strftime("local date and time is: %c"))
#print(now.strftime("local date is: %x"))
#print(now.strftime("local time is: %X"))

# %I/%H - 12/24 Hour, %M - Minute, %S - Second, %p - local AP/PM
#print(now.strftime("Current time is: %I:%M:%S %p"))
#print(now.strftime("Current time is: %H:%M"))

t = datetime.now() - timedelta(weeks=1)
s = t.strftime("%A %B %d, %Y") 
print("One week ago date is: ", s)




from datetime import timedelta

print(timedelta(days=365, hours=5, minutes=1))

now = datetime.now()
print("Current date is: ", now)
print("After one year date is: ", now + timedelta(days=365))
print("After two weeks and 3 days date is: ", now + timedelta(weeks=2, days=3))


#April Fool's Day counting:

from datetime import date
#from datetime import deltatime

today = date.today()
#today = date(today.year, 5, 2)
print(f"Current date is {today}") 

afd = date(today.year, 4, 1)

if afd<today:
    print(f"April fool's day already when by {(today-afd).days} days ago")
    afd = afd.replace(year=today.year+1)

time_to_afd = afd-today
print(f"It's just {time_to_afd.days} days until April Fool's day")
