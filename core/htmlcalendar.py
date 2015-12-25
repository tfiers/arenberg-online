from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from itertools import groupby
from calendar import HTMLCalendar, monthrange
from datetime import date

class Calendar(HTMLCalendar):
    """Renders HTML code for the calendar, needed in core/views.py"""

    def __init__(self, pEvents):
        super(Calendar, self).__init__()
        self.contest_events = self.group_by_day(pEvents)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            today = date.today()
            if today == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.contest_events:
                cssclass += ' filled'
                body = []
                for contest in self.contest_events[day]:
                    if not contest.absolute_url == '':
                        body.append('<a id = "calendarfield" href="%s" target="_blank">' %contest.absolute_url) #open page in new tab
                    else:
                        body.append('<div id="calendarfield">')
                    body.append(esc(contest.name+' @'+contest.location+' '+contest.start_hour.strftime("%H:%M"))) 
                    if not contest.absolute_url == '':
                        body.append('</a><br/>')
                    else:
                        body.append('</div>')
                return self.day_cell(cssclass, '<div class="dayNumber">%d</div> %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, '<div class="dayNumber">%d</div>' % day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(Calendar, self).formatmonth(year, month)

    def group_by_day(self, pEvents): 
        field = lambda eve: eve.date_of_event.day
        return dict([(day, list(items)) for day, items in groupby(pEvents, field)])

    def day_cell(self, cssclass, body): #
        return '<td class="%s">%s</td>' % (cssclass, body)