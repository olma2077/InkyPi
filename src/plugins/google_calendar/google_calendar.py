from plugins.base_plugin.base_plugin import BasePlugin
from ics import Calendar, Event
import requests
from datetime import datetime, timedelta, timezone, time
from dateutil.rrule import rrulestr
from zoneinfo import ZoneInfo
import os
import logging
from dataclasses import dataclass
from PIL import Image

logger = logging.getLogger(__name__)


@dataclass
class CalendarEvent:
    def __init__(self, start_day, start_time, end_day, end_time, text):
        start_day = start_day
        start_time = start_time
        end_day = end_day
        end_time = end_time
        text = text


class GoogleCalendar(BasePlugin):
    tzone = "Europe/Madrid"

    def generate_settings_template(self):
        template_params = super().generate_settings_template()

        return template_params

    def generate_image(self, settings, device_config):


        events = self.get_events(settings.calendars)
        image = self.render_events(events)
        return image

    def get_events(self, calendars, days: int = 2):
        all_events = []

        for calendar in calendars:
            cal = Calendar(requests.get(calendar).text)
            all_events.extend(self.get_calendar_events(cal, days))

        return all_events

    def get_calendar_events(self, calendar, days):
        zone = ZoneInfo(self.tzone)
        start_of_today = datetime.combine(datetime.now(zone), time.min, tzinfo=zone)

        return self.get_events_between(calendar, start_of_today, start_of_today + timedelta(days=days), zone)

    def get_events_between(self, cal: Calendar, start_date: datetime, end_date: datetime, zone: ZoneInfo):
        event_data = []

        def get_day_time(date: datetime):
            date = date.astimezone(zone)
            return ((date - start_date.astimezone(zone)).days, date.hour * 100 + date.minute)

        for event in cal.events:
            rrule_found = False

            for extra in event.extra:
                if extra.name == "RRULE":
                    # if the event is recurring, add every occurrence that lands between the start and end date
                    rrule = extra.value
                    rule = rrulestr(rrule, dtstart=event.begin.datetime)
                    for occurrence_start in rule.between(start_date, end_date):
                        occurrence_end = occurrence_start + (event.end.datetime - event.begin.datetime)
                        event_data.append((*get_day_time(occurrence_start), *get_day_time(occurrence_end), event.name))
                    rrule_found = True
                    break

            if not rrule_found and event.begin <= end_date and start_date <= event.end:
                event_data.append((*get_day_time(event.begin), *get_day_time(event.end), event.name))

        return list(map(lambda edata: CalendarEvent(*edata), event_data))

    def render_events(self, events):
        return Image.new("RGB", (800, 480), (255, 255, 255))  # Placeholder for actual rendering logic
