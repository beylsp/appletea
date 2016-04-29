import json
import os.path as osp
import unittest

from appletea.ipinfo.models import IpInfo


class TestModels(unittest.TestCase):
    def setUp(self):
        json_file = osp.join(
            osp.dirname(osp.abspath(__file__)), 'data/test.json')
        with open(json_file) as fp:
            self.json_data = json.loads(fp.read())
        self.ipinfo = IpInfo(self.json_data)

    def test_get_ipinfo_ip(self):
        self.assertEquals(self.ipinfo.ip, self.json_data['ip'])

    def test_get_ipinfo_hostname(self):
        self.assertEquals(self.ipinfo.hostname, self.json_data['hostname'])

    def test_get_ipinfo_city(self):
        self.assertEquals(self.ipinfo.city, self.json_data['city'])

    def test_get_ipinfo_region(self):
        self.assertEquals(self.ipinfo.region, self.json_data['region'])

    def test_get_ipinfo_country(self):
        self.assertEquals(self.ipinfo.country, self.json_data['country'])

    def test_get_ipinfo_loc(self):
        expected_lat, expected_lng = self.json_data['loc'].split(',')
        lat, lng = self.ipinfo.loc
        self.assertEquals(lat, expected_lat)
        self.assertEquals(lng, expected_lng)

    def test_get_ipinfo_org(self):
        self.assertEquals(self.ipinfo.org, self.json_data['org'])

    def test_get_ipinfo_postal(self):
        self.assertEquals(self.ipinfo.postal, self.json_data['postal'])

    def test_get_ipinfo_invalid_field(self):
        with self.assertRaises(ValueError) as e_cm:
            self.ipinfo.undefined

        self.assertEqual(e_cm.exception.message, 'Property "undefined" not '
                         'valid or is not available for this IP address.')

    def test_get_ipinfo_returns_printable_object(self):
        ip = self.json_data['ip']
        expected_str = '<IpInfo instance: %s>' % ip
        self.assertEqual(str(self.ipinfo), expected_str)
