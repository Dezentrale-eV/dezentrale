# ------------------------------------------------------------------------------
# Joyous template tags
# ------------------------------------------------------------------------------
import datetime as dt
import ls.joyous as calendar
from django import template
from ls.joyous.utils.telltime import timeFormat, dateFormat  #... telltime import ...
from ls.joyous.models import getAllEventsByDay
from ls.joyous.models import getAllUpcomingEvents
from ls.joyous.models import getGroupUpcomingEvents
from ls.joyous.models import getAllEventsByWeek
from ls.joyous.models import CalendarPage
from ls.joyous.utils.weeks import weekday_abbr, weekday_name
from ls.joyous.edit_handlers import MapFieldPanel

register = template.Library()

@register.inclusion_tag("joyous/tags/events_this_week.html",
                        takes_context=True)
# includes also empty days
def events_this_week_german(context):
    """
    Displays a week's worth of events.   Starts week with Monday, unless today is Sunday.
    Uses a template from App Events
    """
    request = context['request']
    home = request.site.root_page
    cal = CalendarPage.objects.live().descendant_of(home).first()
    calUrl = cal.get_url(request) if cal else None
    calName = cal.title if cal else None
    today = dt.date.today()
    beginOrd = today.toordinal()

    if today.weekday() != 6:
         # Start week with Monday, unless today is Sunday
         beginOrd -= today.weekday()
    endOrd = beginOrd + 6
    dateFrom = dt.date.fromordinal(beginOrd)
    dateTo   = dt.date.fromordinal(endOrd)
    if cal:
        events = cal._getEventsByDay(request, dateFrom, dateTo)
    else:
        events = getAllEventsByDay(request, dateFrom, dateTo)
    return {'request':      request,
            'today':        today,
            'calendarUrl':  calUrl,
            'calendarName': calName,
            'events':       events }

@register.inclusion_tag("joyous/tags/events_this_week.html",
                        takes_context=True)
#event-days only fot the next ten days
def events_next_ten_days_german(context):
    """
    Displays upcoming events of next 10 days
    Uses a Template from App Events
    """
    request = context['request']
    home = request.site.root_page
    cal = CalendarPage.objects.live().descendant_of(home).first()
    calUrl = cal.get_url(request) if cal else None
    calName = cal.title if cal else None
    today = dt.date.today()
    beginOrd = today.toordinal()
    #if today.weekday() != 6:
        # Start week with Monday, unless today is Sunday
    #    beginOrd -= today.weekday()
    endOrd = beginOrd + 10 # number of days (here ten)
    dateFrom = dt.date.fromordinal(beginOrd)
    dateTo   = dt.date.fromordinal(endOrd)
    if cal:
        events = cal._getEventsByDay(request, dateFrom, dateTo)
    else:
        events = getAllEventsByDay(request, dateFrom, dateTo)

    #Filter eventsOnly, then make dict from that
    eventsOnly = []
    i=0
    while i<len(events):        
        #events[i]: EventsOnDay(date=datetime.date(2019, 5, 12), days_events=[], continuing_events=[])
        #type: class 'ls.joyous.models.events.EventsOnDay',
        days_events=events[i].days_events        # type: list
        continuing_events=events[i].continuing_events # type: list
        # print(type(days_events))
        # print(type(continuing_events))
        if len(days_events) == 0 and len(continuing_events)==0:
            i+=1
        else:
            eventsOnly.append(events[i])
            i+=1

    #output , Type: dict
    output = {'request':      request,
            'today':        today,
            'calendarUrl':  calUrl,
            'calendarName': calName,
            'events':       eventsOnly } #Orig: events (with events also empty days are included)
    return output


# @register.inclusion_tag("joyous/tags/minicalendar.html",
#                         takes_context=True)
# def minicalendar(context):
#     """
#     Displays a little ajax version of the joyous.
#     """
#     today = dt.date.today()
#     request = context['request']
#     home = request.site.root_page
#     cal = CalendarPage.objects.live().descendant_of(home).first()
#     calUrl = cal.get_url(request) if cal else None
#     if cal:
#         events = cal._getEventsByWeek(request, today.year, today.month)
#     else:
#         events = getAllEventsByWeek(request, today.year, today.month)
#     return {'request':     request,
#             'today':       today,
#             'year':        today.year,
#             'month':       today.month,
#             'calendarUrl': calUrl,
#             'monthName':   calendar.month_name[today.month],
#             'weekdayInfo': zip(weekday_abbr, weekday_name),
#             'events':      events}

# @register.inclusion_tag("joyous/tags/upcoming_events_detailed.html",
#                         takes_context=True)
# def all_upcoming_events_alt(context):
#     """
#     Displays a list of all upcoming events.
#     """
#     request = context['request']
#     return {'request': request,
#             'events':  getAllUpcomingEvents(request)}
#
# @register.inclusion_tag("joyous/tags/upcoming_events_detailed.html",
#                         takes_context=True)
# def subsite_upcoming_events_alt(context):
#     """
#     Displays a list of all upcoming events in this site.
#     """
#     request = context['request']
#     home = request.site.root_page
#     return {'request': request,
#             'events':  getAllUpcomingEvents(request, home=home)}
#
# @register.inclusion_tag("joyous/tags/upcoming_events_list.html",
#                         takes_context=True)
# def group_upcoming_events_alt(context, group=None):
#     """
#     Displays a list of all upcoming events that are assigned to a specific
#     group.  If the group is not specified it is assumed to be the current page.
#     """
#     request = context.get('request')
#     if group is None:
#         group = context.get('page')
#     if group:
#         events = getGroupUpcomingEvents(request, group)
#     else:
#         events = []
#     return {'request': request,
#             'events':  events}
#
# @register.inclusion_tag("joyous/tags/future_exceptions_list.html",
#                         takes_context=True)
# def future_exceptions_alt(context, rrevent=None):
#     """
#     Displays a list of all the future exceptions (extra info, cancellations and
#     postponements) for a recurring event.  If the recurring event is not
#     specified it is assumed to be the current page.
#     """
#     request = context['request']
#     if rrevent is None:
#         rrevent = context.get('page')
#     if rrevent:
#         exceptions = rrevent._futureExceptions(request)
#     else:
#         exceptions = []
#     return {'request':    request,
#             'exceptions': exceptions}
#
# @register.simple_tag(takes_context=True)
# def next_on_alt(context, rrevent=None):
#     """
#     Displays when the next occurence of a recurring event will be.  If the
#     recurring event is not specified it is assumed to be the current page.
#     """
#     request = context['request']
#     if rrevent is None:
#         rrevent = context.get('page')
#     eventNextOn = getattr(rrevent, '_nextOn', lambda _:None)
#     return eventNextOn(request)
#
# @register.inclusion_tag("joyous/tags/location_gmap.html",
#                         takes_context=True)
# # Could make this a simple_tag, but would then need to
# # watch out for unsafe HTML
# def location_gmap_alt(context, location):
#     """Display a link to Google maps iff we are using WagtailGMaps"""
#     gmapq = None
#     if getattr(MapFieldPanel, "UsingWagtailGMaps", False):
#         gmapq = location
#     return {'gmapq': gmapq}
#
# # ------------------------------------------------------------------------------
# # Format times and dates e.g. on event page
# @register.filter
# def time_display_alt(time):
#     """format the time in a readable way"""
#     return timeFormat(time)
#
# @register.filter
# def at_time_display_alt(time):
#     """format as being "at" some time"""
#     return timeFormat(time, prefix=_("at "))
#
# @register.filter
# def date_display_alt(date):
#     """format the date in a readable way"""
#     return dateFormat(date)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
