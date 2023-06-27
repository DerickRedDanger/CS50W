from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .. import models




class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None,):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()
		
	# formats a day as a td
	# filter events by day
	def formatday(self, day, events,today):
		if today == 1:
			today=datetime.today().day
		events_per_day = events.filter(day__day=day).order_by('start_time')
		d = ''
		for event in events_per_day:
			d += f'<li> {event.title} </li>'

		if day != 0:
			if day == today:
				return f"<td><span class='date' style='color:red' >{day} - Today </span><ul> {d} </ul></td>"
			else:
				return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events,today):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events,today)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = models.Event.objects.filter(day__year=self.year, day__month=self.month)


		thisM=datetime.today()
		if self.year == thisM.year and  self.month == thisM.month:
			today = 1
		else:
			today = 0


		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events,today)}\n'
		return cal