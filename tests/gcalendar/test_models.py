import json
import os.path as osp
import unittest

from appletea.gcalendar.models import GCalendarEvents


class TestModels(unittest.TestCase):
    def _readf(self, f):
        with open(f) as fp:
            data = json.loads(fp.read())
        return data

    @property
    def json_data(self):
        json_data = osp.join(osp.dirname(osp.abspath(__file__)),
                             'data/calendar-events.json')
        return self._readf(json_data)

    @property
    def items(self):
        return self.json_data['items']

    def test_gcalendarevents_with_empty_json(self):
        self.gcal = GCalendarEvents({})
        self.assertEqual(len(self.gcal.events), 0)

    def test_gcalendarevents_with_empty_item_list(self):
        self.gcal = GCalendarEvents({'items': []})
        self.assertEqual(len(self.gcal.events), 0)

    def test_gcalendarevents_with_json_string(self):
        self.gcal = GCalendarEvents(self.json_data)
        self.assertEqual(len(self.gcal.events), len(self.items))

    def test_gcalendarevents_with_valid_string_property(self):
        self.gcal = GCalendarEvents(self.json_data)
        self.assertEqual(self.gcal.events[0].summary, self.items[0]['summary'])

    def test_gcalendarevents_with_invalid_string_property(self):
        self.gcal = GCalendarEvents(self.json_data)
        with self.assertRaises(ValueError) as e_cm:
            self.gcal.events[0].undefined
        self.assertEqual(str(e_cm.exception), 'Property "undefined" not '
                         'valid or is not available for event item.')

    def test_gcalendarevents_with_valid_list_property(self):
        self.gcal = GCalendarEvents(self.json_data)
        self.assertIsInstance(self.gcal.events[0].attendees, list)

    def test_gcalendarevents_with_valid_list_property_item(self):
        self.gcal = GCalendarEvents(self.json_data)
        self.assertEquals(self.gcal.events[0].attendees[0].email, self.items[0]['attendees'][0]['email'])

    def test_gcalendarevents_with_invalid_list_property_item(self):
        self.gcal = GCalendarEvents(self.json_data)
        with self.assertRaises(ValueError) as e_cm:
            self.gcal.events[0].attendees[0].undefined
        self.assertEqual(str(e_cm.exception), 'Property "undefined" not '
                         'valid or is not available for event item "attendees".')

    def test_gcalendarevents_with_valid_dict_property_item(self):
        self.gcal = GCalendarEvents(self.json_data)
        self.assertEquals(self.gcal.events[0].start.dateTime, self.items[0]['start']['dateTime'])

    def test_gcalendarevents_with_invalid_dict_property_item(self):
        self.gcal = GCalendarEvents(self.json_data)
        with self.assertRaises(ValueError) as e_cm:
            self.gcal.events[0].start.undefined
        self.assertEqual(str(e_cm.exception), 'Property "undefined" not '
                         'valid or is not available for event item "start".')

    def test_gcalendarevents_returns_printable_data_object_list(self):
        self.gcal = GCalendarEvents(self.json_data)
        expected_str = '<GCalendarEvents instance with %d events>' % len(self.items)
        self.assertEqual(str(self.gcal), expected_str)

    def test_gcalendarevents_returns_printable_data_object(self):
        self.gcal = GCalendarEvents(self.json_data)
        expected_str = '<GEventData instance: organizer>'
        self.assertEqual(str(self.gcal.events[0].organizer), expected_str)
