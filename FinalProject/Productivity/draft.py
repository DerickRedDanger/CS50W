from datetime import datetime, timedelta

#x = datetime(2020, 5, 17)
d = datetime.now()

print(d.month)
print(d.year)
print(d.strftime("%A"))
previous_m= d.month-1

first = d.replace(day=1)
prev_month = first - timedelta(days=1)
pmonth = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)

print(first)
print(prev_month)
print(pmonth)
print(previous_m)

mont = d.month + 1
next_month = d.replace(year=d.year, month=mont, day=1)
nmonth = 'month=' + str(next_month.year) + '-' + str(next_month.month)
#days_in_month = HTMLCalendar.monthrange(x.year, x.month)[1]
#last = x.replace(day=days_in_month)
#next_month = last + timedelta(days=1)
print(mont)
#print(days_in_month)
#print(last)
print(next_month)
print(nmonth)