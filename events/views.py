from django.shortcuts import render
from wagtail.core.models import Page
from django.http import JsonResponse
import json
# TODO: Fix JSON
def getEvents(request):
    events = {"events": {}}
    events_page = Page.objects.get(title="Kalender").get_children().live()
    for item in events_page:
        events["events"][str(item.specific.title)] = {'start_time': str(item.specific.time_from),
                                       'end_time':str(item.specific.time_to), 
                                       'description':str(item.specific.details)}
    return JsonResponse(json.dumps(events), safe=False)
