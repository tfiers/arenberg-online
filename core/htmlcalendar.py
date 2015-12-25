from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from itertools import groupby
from calendar import HTMLCalendar, monthrange
from datetime import date

class Calendar(HTMLCalendar):
    """Renders HTML code for the calendar, needed in core/views.py"""

    def __init__(self, pEvents):
        super(Calendar, self).__init__()
        self.events = self.group_by_day(pEvents)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            today = date.today()
            if today == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                body = []
                for e in self.events[day]:
                    #there could be a bug in here, if second if is made an elif, every 1 show up again in the style of 5
                    #added extra %s for formatting with calendarfield styles
                    if e.event_color == "1" or e.event_color == "2" or e.event_color == "3": #repetitie, concert en event
                        if not e.absolute_url == '':
                            body.append('<a id = "calendarfield%s" href="%s" target="_blank">' %(e.event_color,e.absolute_url)) #opens the page in new tab, calenderfield id for css
                        else:
                            body.append('<div id="calendarfield%s">' %e.event_color)
                        body.append(esc(e.name+' @'+e.location+' '+e.start_hour.strftime("%H:%M"))) 
                        if not e.absolute_url == '':
                            body.append('</a><br/>')
                        else:
                            body.append('</div>')
                    elif e.event_color == "5": #weekend: zelfde opmaak als 1 maar zegt enkel repetitie
                        if not e.absolute_url == '':
                            body.append('<a id = "calendarfield%s" href="%s" target="_blank">' %(e.event_color,e.absolute_url)) #opens the page in new tab, calenderfield id for css
                        else:
                            body.append('<div id="calendarfield%s">' %e.event_color)
                        body.append(esc(e.name)) 
                        if not e.absolute_url == '':
                            body.append('</a><br/>')
                        else:
                            body.append('</div>')
                    else: #4: birthdays and events
                        if not e.absolute_url == '':
                            body.append('<a id = "calendarfield%s" href="%s" target="_blank">' %(e.event_color,e.absolute_url)) #opens the page in new tab, calenderfield id for css
                        else:
                            body.append('<div id="calendarfield%s">' %e.event_color)
                        body.append(esc(e.name)) #voor verjaardag 
                        if not e.absolute_url == '':
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

    def sort_by_hour(self,pEvents):
        return sorted

    def day_cell(self, cssclass, body): 
        return '<td class="%s">%s</td>' % (cssclass, body)