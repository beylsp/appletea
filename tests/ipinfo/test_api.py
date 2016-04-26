import mock
import requests
import requests_mock
import unittest

from appletea import ipinfo
from appletea.ipinfo.models import IpInfo


class TestApi(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://ipinfo.io'

    @requests_mock.Mocker()
    def test_get_ipinfo_raises_client_error_404(self, mock):
        mock.get(requests_mock.ANY, status_code=404, json={})
        with self.assertRaises(requests.HTTPError) as e_cm:
            ipinfo.get_ipinfo()

        self.assertEquals(e_cm.exception.response.status_code, 404)

    @requests_mock.Mocker()
    def test_get_ipinfo_raises_server_error_503(self, mock):
        mock.get(requests_mock.ANY, status_code=503, json={})
        with self.assertRaises(requests.HTTPError) as e_cm:
            ipinfo.get_ipinfo()

        self.assertEquals(e_cm.exception.response.status_code, 503)

    def test_get_ipinfo_sets_correct_connect_timeout(self):
        def requests_get_mock(*args, **kwargs):
            self.assertEquals(kwargs.get('timeout'), 5)

            with requests.sessions.Session() as session:
                from requests.packages import urllib3
                urllib3.disable_warnings()
                return requests_mock.create_response(
                    session.request('GET', args[0]), content={})

        with mock.patch('requests.get', requests_get_mock):
            ipinfo.get_ipinfo()

    @requests_mock.Mocker()
    def test_get_ipinfo_calls_correct_url(self, mock):
        mock.get(requests_mock.ANY, json={})
        ipinfo.get_ipinfo()

        expected_url = '%s/json' % self.baseurl
        url = '%s://%s/%s' % (mock.last_request.scheme,
                              mock.last_request.netloc, 'json')
        self.assertEquals(url, expected_url)

    @requests_mock.Mocker()
    def test_get_ipinfo_calls_correct_url_with_ip(self, mock):
        mock.get(requests_mock.ANY, json={})
        ip_address = '8.8.8.8'
        ipinfo.get_ipinfo(ip=ip_address)

        expected_url = '%s/%s/json' % (self.baseurl, ip_address)
        url = '%s://%s/%s/json' % (mock.last_request.scheme,
                                   mock.last_request.netloc, ip_address)
        self.assertEquals(url, expected_url)

    @requests_mock.Mocker()
    def test_get_ipinfo_calls_correct_url_with_param(self, mock):
        mock.get(requests_mock.ANY, json={})
        parameter = 'region'
        ipinfo.get_ipinfo(param=parameter)

        expected_url = '%s/%s' % (self.baseurl, parameter)
        url = '%s://%s/%s' % (mock.last_request.scheme,
                              mock.last_request.netloc, parameter)
        self.assertEquals(url, expected_url)

    @requests_mock.Mocker()
    def test_get_ipinfo_calls_correct_url_with_ip_and_param(self, mock):
        mock.get(requests_mock.ANY, json={})
        ip_address = '8.8.8.8'
        parameter = 'region'
        ipinfo.get_ipinfo(ip=ip_address, param=parameter)

        expected_url = '%s/%s/%s' % (self.baseurl, ip_address, parameter)
        url = '%s://%s/%s/%s' % (mock.last_request.scheme,
                                 mock.last_request.netloc, ip_address, parameter)
        self.assertEquals(url, expected_url)

    @requests_mock.Mocker()
    def test_get_ipinfo_returns_object_model_for_json(self, mock):
        mock.get(requests_mock.ANY, json={})
        r = ipinfo.get_ipinfo()

        self.assertIsInstance(r, IpInfo)

    @requests_mock.Mocker()
    def test_get_ipinfo_returns_object_model_for_field(self, mock):
        mock.get(requests_mock.ANY, text='')
        r = ipinfo.get_ipinfo(param='region')

        self.assertIsInstance(r, IpInfo)
