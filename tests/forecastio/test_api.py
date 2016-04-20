import requests
import requests_mock
import unittest
import urllib2

from appletea import forecastio


@requests_mock.Mocker()
class TestApi(unittest.TestCase):

    def test_get_forecast_raises_client_error_404(self, mock):
        mock.get(requests_mock.ANY,
                 status_code=requests.codes.not_found, json={})
        with self.assertRaises(requests.HTTPError) as e_cm:
            forecastio.get_forecast(key='238ff8ab86e8245aa668b9d9cf8e8', 
                                    latitude=51.036391, longitude=3.699794)
        self.assertEquals(e_cm.exception.response.status_code, 
                          requests.codes.not_found)

    def test_get_forecast_raises_server_error_503(self, mock):
        mock.get(requests_mock.ANY,
                 status_code=requests.codes.service_unavailable, json={})
        with self.assertRaises(requests.HTTPError) as e_cm:
            forecastio.get_forecast(key='238ff8ab86e8245aa668b9d9cf8e8', 
                                    latitude=51.036391, longitude=3.699794)
        self.assertEquals(e_cm.exception.response.status_code, 
                          requests.codes.service_unavailable)
