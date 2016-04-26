import unittest

from appletea import ipinfo
from appletea.ipinfo.models import IpInfo


class TestModels(unittest.TestCase):
    def setUp(self):
        self.json = {
            "ip": "8.8.8.8",
            "hostname": "google-public-dns-a.google.com",
            "city": "Mountain View",
            "region": "California",
            "country": "US",
            "loc": "37.3845,-122.0881",
            "org": "AS15169 Google Inc.",
            "postal": "94040"
        }
        self.ipinfo = IpInfo(self.json)

    def test_get_ipinfo_ip(self):
        self.assertEquals(self.ipinfo.ip, self.json['ip'])

    def test_get_ipinfo_hostname(self):
        self.assertEquals(self.ipinfo.hostname, self.json['hostname'])

    def test_get_ipinfo_city(self):
        self.assertEquals(self.ipinfo.city, self.json['city'])

    def test_get_ipinfo_region(self):
        self.assertEquals(self.ipinfo.region, self.json['region'])

    def test_get_ipinfo_country(self):
        self.assertEquals(self.ipinfo.country, self.json['country'])

    def test_get_ipinfo_loc(self):
        expected_lat, expected_lng = self.json['loc'].split(',')
        lat, lng = self.ipinfo.loc
        self.assertEquals(lat, expected_lat)
        self.assertEquals(lng, expected_lng)

    def test_get_ipinfo_org(self):
        self.assertEquals(self.ipinfo.org, self.json['org'])

    def test_get_ipinfo_postal(self):
        self.assertEquals(self.ipinfo.postal, self.json['postal'])

    def test_get_ipinfo_invalid_field(self):
        with self.assertRaises(ValueError) as e_cm:
            self.ipinfo.undefined
        
        print dir(e_cm.exception)
        self.assertEqual(e_cm.exception.message, 'Property "undefined" not '
                         'valid or is not available for this IP address.')
