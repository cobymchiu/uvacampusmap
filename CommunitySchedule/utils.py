# Hui Wen
# Date made: 24 July 2018
# Web browser Calendar source code
# https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html 
from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import CommunityEvent
from django.contrib.auth.decorators import login_required

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day=day)
		d = ''
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = CommunityEvent.objects.filter(start_time__year=self.year, start_time__month=self.month)
		schedule = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		schedule += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		schedule += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			schedule += f'{self.formatweek(week, events)}\n'
		return schedule
	# Hui Wen
# Date made: 24 July 2018
# Web browser Calendar source code
# https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html 
