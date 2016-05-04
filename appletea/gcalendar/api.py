import apiclient as api
import httplib2
import oauth2client as oauth2

from appletea.gcalendar.models import GCalendarEvents


def get_events(credentials, **kwargs):
    credentials = oauth2.client.OAuth2Credentials.from_json(credentials)
    http = credentials.authorize(httplib2.Http())
    service = api.discovery.build('calendar', 'v3', http=http)

    kwargs.setdefault('orderBy', 'startTime')
    request = service.events().list(calendarId='primary', **kwargs)
    eventsResult = request.execute(http=http)

    return GCalendarEvents(eventsResult)
