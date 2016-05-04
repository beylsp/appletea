import apiclient
import mock
import os.path as osp
import unittest
import urlparse

from appletea import gcalendar
from appletea.gcalendar.models import GCalendarEvents
from collections import OrderedDict as odict


class TestApi(unittest.TestCase):
    def _readf(self, f):
        with open(f) as fp:
            data = fp.read()
        return data

    @property
    def credentials(self):
        credentials = osp.join(
            osp.dirname(osp.abspath(__file__)),
            'data/application-default-credentials.json')
        return self._readf(credentials)

    def test_get_events_return_object_model(self):
        def request_execute_mock(request, **kwargs):
            return {}

        with mock.patch('apiclient.http.HttpRequest.execute',
                        request_execute_mock):
            events = gcalendar.get_events(self.credentials)

        self.assertIsInstance(events, GCalendarEvents)

    def test_get_events_calls_correct_url(self):
        def request_execute_mock(request, **kwargs):
            urlres = urlparse.urlparse(request.uri)
            qs = urlparse.parse_qs(urlres.query)
            expected_qs = {u'alt': [u'json'], u'orderBy': [u'startTime']}

            self.assertDictEqual(qs, expected_qs)
            return {}

        with mock.patch('apiclient.http.HttpRequest.execute',
                        request_execute_mock):
            gcalendar.get_events(self.credentials)

    def test_get_events_calls_correct_url_with_orderBy(self):
        def request_execute_mock(request, **kwargs):
            urlres = urlparse.urlparse(request.uri)
            qs = urlparse.parse_qs(urlres.query)
            expected_qs = {u'alt': [u'json'], u'orderBy': [u'updated']}

            self.assertDictEqual(qs, expected_qs)
            return {}

        with mock.patch('apiclient.http.HttpRequest.execute',
                        request_execute_mock):
            gcalendar.get_events(self.credentials, orderBy='updated')

    def test_get_events_calls_correct_url_with_multi_argument(self):
        def request_execute_mock(request, **kwargs):
            urlres = urlparse.urlparse(request.uri)
            qs = urlparse.parse_qs(urlres.query)
            expected_qs = {u'orderBy': [u'startTime'],
                           u'timeMin': [u'2011-06-03T10:00:00Z'],
                           u'timeMax': [u'2011-06-03T10:00:00Z'],
                           u'alt': [u'json'], u'singleEvents': [u'true'],
                           u'maxAttendees': [u'5']}

            self.assertDictEqual(qs, expected_qs)
            return {}

        with mock.patch('apiclient.http.HttpRequest.execute',
                        request_execute_mock):
            gcalendar.get_events(
                self.credentials, maxAttendees=5, timeMax='2011-06-03T10:00:00Z',
                timeMin='2011-06-03T10:00:00Z', singleEvents=True)
            
