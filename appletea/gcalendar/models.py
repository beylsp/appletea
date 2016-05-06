"""Google Calendar Events object model.

Events object model for Google Calendar API responses.
"""
from appletea.utils import UnicodeMixin
from appletea.exceptions import HTTPError


class GCalendarEvents(UnicodeMixin):
    """GCalendarEvents data object.

    Google Calendar Events data object includes a list of events information.
    """
    def __init__(self, json):
        self._raise_for_status(json.get('error', ''))
        self.json = json
        self.events = [GEventData(item) for item in json.get('items', [])]

    def _raise_for_status(self, e):
        if e:
            status_code = e.get('code', None)
            reason = e.get('message', '')

            if 400 <= status_code < 500:
                http_error_msg = '%s Client Error: %s' % (status_code, reason)
            elif 500 <= status_code < 600:
                http_error_msg = '%s Server Error: %s' % (status_code, reason)
            else:
                http_error_msg = 'Undefined Error'

            raise HTTPError(http_error_msg)

    def __unicode__(self):
        return ('<GCalendarEvents instance with %d events>' % len(self.events))


class GEventData(UnicodeMixin):
    """GEventData data object.

    An event data object represents an Event Resource on a particular calendar.
    Such objects contain various properties. More information can be found at:

    https://developers.google.com/google-apps/calendar/v3/reference/events#resource-representations
    """
    def __init__(self, d={}, supitem=''):
        self.supitem = supitem
        self.d = d

    def __getattr__(self, name):
        try:
            v = self.d[name]
            if isinstance(v, dict):
                return GEventData(v, name)
            elif isinstance(v, list):
                return [GEventData(x, name) for x in v]
            else:
                return v
        except KeyError:
            raise ValueError(
                'Property "%s" not valid or is not available for event'
                ' %s.' % (
                    name,
                    'item "%s"' % self.supitem if self.supitem else 'item'))

    def __unicode__(self):
        return ('<GEventData instance: %s>' % self.supitem)
