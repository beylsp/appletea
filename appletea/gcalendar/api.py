"""Client for google calendar APIs.

A REST client library for google calendar APIs.
"""
import apiclient as api
import httplib2
import oauth2client as oauth2

from appletea.gcalendar.models import GCalendarEvents


def get_events(credentials, calendarId='primary', **kwargs):
    """Return google calendar events for on the specified calendar.

    Return a google calendar object for given credentials and calendar
    identifier.

    A calendar is a collection of events, along with additional metadata such
    as summary, default time zone, location, etc. Each calendar is identified
    by an ID which is an email address. A primary calendar is a special type
    of calendar associated with a single user account.

    To request event data, your application needs the scope information, as
    well as information that Google supplies when you register your
    application (such as the client ID and the client secret). This must all
    be packed in the credentials object. Additional arguments can be:

      - alwaysIncludeEmail: Whether to always include a value in the email
        field (default: False).
      - iCalUID: Specifies event ID in the iCalendar format.
      - maxAttendees: The maximum number of attendees to include in the
        response.
      - maxResults: Maximum number of events returned on one result page
        (default: 250).
      - orderBy: The order of the events returned in the result: "startTime" or
        "updated" (default: "startTime").
      - pageToken: Token specifying which result page to return.
      - privateExtendedProperty: Extended properties constraint specified as
        propertyName=value. Matches only private properties.
      - q: Free text search terms.
      - sharedExtendedProperty: Extended properties constraint specified as
        propertyName=value. Matches only shared properties.
      - showDeleted: Whether to include deleted events in the result.
      - showHiddenInvitations: Whether to include hidden invitations in the
        result.
      - singleEvents: Whether to only return single one-off events and
        instances of recurring events (default: False).
      - syncToken: Token obtained from the nextSyncToken field.
      - timeMax: Upper bound (exclusive) for an event's start time to
        filter by (RFC3339 timestamp with mandatory offset).
      - timeMin: Lower bound (inclusive) for an event's end time to filter by
        (RFC3339 timestamp with mandatory offset).
      - timeZone: Time zone used in the response.
      - updatedMin: Lower bound for an event's last modification time to
        filter by.

    Args:
      - credentials: Oauth2.0 crendentials object.
      - calendarId: calendar identifier. If you want to access the primary
        calendar of the currently logged in user, use the "primary" keyword
        (=default).
      - kwargs: additional arguments passed as query params to service API.

    Returns:
      A google calendar events object with methods for accessing its data.

    Raises:
      An HTTPError when a bad request is made.
    """
    credentials = oauth2.client.OAuth2Credentials.from_json(credentials)
    service = api.discovery.build('calendar', 'v3', credentials=credentials)

    kwargs.setdefault('orderBy', 'startTime')
    result = service.events().list(calendarId=calendarId, **kwargs).execute()

    return GCalendarEvents(result)
