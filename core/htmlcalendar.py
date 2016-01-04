from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from itertools import groupby
from calendar import HTMLCalendar, monthrange
from datetime import date

class Calendar(HTMLCalendar):
    """
    Renders HTML code for the calendar, needed in core/views.py.

    Make sure to escape every possible bit of database info (like esc(e.name)): to be protect against xss attacks.
    """

    def __init__(self, pEvents, birthdays):
        super(Calendar, self).__init__()
        self.events = self.group_by_day(pEvents)
        self.bdays = self.group_by_day_bday(birthdays)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            today = date.today()
            if today == date(self.year, self.month, day):
                cssclass += ' today'
            body = []
            body.append('<div style="overflow-y: auto; height:100px">')
            if day in self.events:
                cssclass += ' filled'
                for e in self.events[day]: 
                    #there could be a bug in here, if second if is made an elif, every 1 show up again in the style of 5
                    #added extra %s for formatting with calendarfield styles
                    if e.event_color == "1" or e.event_color == "2" or e.event_color == "3": #repetitie, concert en event
                        #if there's a real url
                        if not e.absolute_url == '' and not e.absolute_url == None:
                            body.append('<div id="calendarfield%s"><a href="%s" target="_blank">' %(e.event_color,e.absolute_url)) #opens the page in new tab, calenderfield id for css
                            body.append(esc(e.name+' @'+e.location+' '+e.start_hour.strftime("%H:%M")+'-'+e.end_hour.strftime("%H:%M"))) 
                            body.append('</a></div>')
                        #else render without "a" tag
                        else:
                            body.append('<div id="calendarfield%s">' %e.event_color)
                            body.append(esc(e.name+' @'+e.location+' '+e.start_hour.strftime("%H:%M")+'-'+e.end_hour.strftime("%H:%M"))) 
                            body.append('</div>')
                    
                    elif e.event_color == "5": #weekend: zelfde opmaak als 1 maar zegt enkel "repetitieweekend"
                        #if there's a real url
                        if not e.absolute_url == '' and not e.absolute_url == None:
                            body.append('<div id="calendarfield%s"><a href="%s" target="_blank">' %(e.event_color,e.absolute_url)) #opens the page in new tab, calenderfield id for css
                            body.append(esc(e.name))
                            body.append('</a>')
                        #else render without "a" tag
                        else:
                            body.append('<div id="calendarfield%s">' %e.event_color)
                            body.append(esc(e.name)) 
                            body.append('</div>')
                body.append('</div>')
                return self.day_cell(cssclass, '<div class="dayNumber">%d</div> %s' % (day, ''.join(body)))

            if day in self.bdays:
                cssclass += ' filled'
                for b in self.bdays[day]:
                    body.append('<div id="calendarfield%s">' %b.event_color)
                    body.append('Birthday ')
                    body.append(esc(b.name)) #voor verjaardag 
                    body.append('</div>')

                body.append('</div>')
                return self.day_cell(cssclass, '<div class="dayNumber">%d</div> %s' % (day, ''.join(body)))
            body.append('</div>')
            return self.day_cell(cssclass, '<div class="dayNumber">%d</div>' % day)
            
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(Calendar, self).formatmonth(year, month)

    def group_by_day(self, pEvents): 
        field = lambda eve: eve.date_of_event.day 
        return dict([(day, list(items)) for day, items in groupby(pEvents, field)])

    def group_by_day_bday(self,birthdays):
        field = lambda eve: eve.date_of_event.day
        return dict([(day, list(items)) for day, items in groupby(birthdays, field)])

    def sort_by_hour(self,pEvents):
        return sorted

    def day_cell(self, cssclass, body): 
        return '<td class="%s">%s</td>' % (cssclass, body)
