from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page

from ls.joyous.models import CalendarPage

# Create a demo version of the Calendar
CalendarPage.is_creatable = False


class CalendarPage(CalendarPage):
    class Meta:
        proxy = True
        verbose_name = "Calendar"

    subpage_types = ['joyous.SimpleEventPage',
                     'joyous.MultidayEventPage',
                     'joyous.RecurringEventPage']

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these pages
        return super().can_create_at(parent) and not cls.objects.exists()
