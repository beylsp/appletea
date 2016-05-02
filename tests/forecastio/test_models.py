import datetime
import json
import os.path as osp
import requests
import requests_mock
import unittest

from appletea.forecastio.models import (
    Forecast, ForecastioDataPoint, ForecastioDataBlock, Alert)


class TestModels(unittest.TestCase):
    def setUp(self):
        response = requests.Response()
        json_file = osp.join(
            osp.dirname(osp.abspath(__file__)), 'data/forecast.json')
        with open(json_file) as fp:
            self.json_data = json.loads(fp.read())
        self.forecast = Forecast(self.json_data, response)

    def test_get_currently_forecast_returns_data_point_object(self):
        self.assertIsInstance(self.forecast.currently, ForecastioDataPoint)

    def test_get_minutely_forecast_returns_data_block_object(self):
        self.assertIsInstance(self.forecast.minutely, ForecastioDataBlock)

    def test_get_minutely_forecast_returns_data_block_object_with_data(self):
        data = self.forecast.minutely.data
        self.assertTrue(all(isinstance(d, ForecastioDataPoint) for d in data))

    def test_get_hourly_forecast_returns_data_block_object(self):
        self.assertIsInstance(self.forecast.hourly, ForecastioDataBlock)

    def test_get_hourly_forecast_returns_data_block_object_with_data(self):
        data = self.forecast.hourly.data
        self.assertTrue(all(isinstance(d, ForecastioDataPoint) for d in data))

    def test_get_daily_forecast_returns_data_block_object(self):
        self.assertIsInstance(self.forecast.daily, ForecastioDataBlock)

    def test_get_daily_forecast_returns_data_block_object_with_data(self):
        data = self.forecast.daily.data
        self.assertTrue(all(isinstance(d, ForecastioDataPoint) for d in data))

    def test_get_alerts_forecast_returns_alert_object_list(self):
        self.assertIsInstance(self.forecast.alerts, list)

    def test_get_alerts_forecast_returns_alert_object_list_with_data(self):
        alerts = self.forecast.alerts
        self.assertTrue(all(isinstance(alert, Alert) for alert in alerts))

    def test_get_alerts_forecast_returns_alert_object_with_valid_data_property(self):
        alerts = self.json_data['alerts']
        title = alerts[0]['title']
        self.assertEqual(self.forecast.alerts[0].title, title)

    def test_get_alerts_forecast_returns_alert_object_with_invalid_data_property(self):
        with self.assertRaises(ValueError) as e_cm:
            self.forecast.alerts[0].undefined
        self.assertEqual(str(e_cm.exception), 'Property "undefined" not '
                         'valid or is not available for this forecast.')

    def test_get_alerts_forecast_returns_printable_object(self):
        alerts = self.json_data['alerts']
        title = alerts[0]['title']
        expires = datetime.datetime.utcfromtimestamp(int(alerts[0]['expires']))
        expected_str = '<Alert instance: %s at %s>' % (title, expires)
        self.assertEqual(str(self.forecast.alerts[0]), expected_str)

    def test_get_currently_forecast_returns_printable_data_point_object(self):
        d = self.json_data['currently']
        time = datetime.datetime.utcfromtimestamp(int(d['time']))
        summary = d['summary']
        expected_str = '<ForecastioDataPoint instance: %s at %s>' % (
            summary, time)
        self.assertEqual(str(self.forecast.currently), expected_str)

    def test_get_minutely_forecast_returns_printable_data_block_object(self):
        d = self.json_data['minutely']
        summary = d['summary']
        length = len(d['data'])
        expected_str = '<ForecastioDataBlock instance: %s with %d' \
                       ' ForecastioDataPoints>' % (summary, length)
        self.assertEqual(str(self.forecast.minutely), expected_str)

    def test_get_currently_forecast_returns_accessible_data_point_object(self):
        temperature = self.json_data['currently']['temperature']
        self.assertEqual(self.forecast.currently.temperature, temperature)

    def test_get_minutely_forecast_returns_accessible_data_block_object(self):
        data = self.json_data['minutely']['data']
        self.assertEqual(len(self.forecast.minutely.data), len(data))

    def test_get_hourly_forecast_returns_accessible_data_block_object(self):
        data = self.json_data['hourly']['data']
        self.assertEqual(len(self.forecast.hourly.data), len(data))

    def test_get_daily_forecast_returns_accessible_data_block_object(self):
        data = self.json_data['daily']['data']
        self.assertEqual(len(self.forecast.daily.data), len(data))

    def test_get_daily_forecast_returns_data_block_object_with_valid_data_property(self):
        data = self.json_data['daily']['data']
        dewPoint = data[0]['dewPoint']
        self.assertEqual(self.forecast.daily.data[0].dewPoint, dewPoint)

    def test_get_daily_forecast_returns_data_block_object_with_invalid_data_property(self):
        with self.assertRaises(ValueError) as e_cm:
            self.forecast.daily.data[0].undefined
        self.assertEqual(str(e_cm.exception), 'Property "undefined" not '
                         'valid or is not available for this forecast.')


class TestModelsEmptyData(unittest.TestCase):
    def setUp(self):
        json_file = osp.join(
            osp.dirname(osp.abspath(__file__)), 'data/forecast.json')
        with open(json_file) as fp:
            self.json_data = json.loads(fp.read())
        self.forecast = Forecast({}, self.create_response())

    def create_response(self):
        baseurl = 'https://api2.forecast.io/forecast'
        apikey = '238ff8ab86e8245aa668b9d9cf8e8'
        latitude = 51.036391
        longitude = 3.699794

        response = requests.Response()
        response.url = '%s/%s/%s,%s' % (
            baseurl, apikey, latitude, longitude)
        return response

    @requests_mock.Mocker()
    def test_get_currently_forecast_reloads_and_returns_data_point_object(self, mock):
        mock.get(requests_mock.ANY, json=self.json_data)
        self.assertIsInstance(self.forecast.currently, ForecastioDataPoint)

    @requests_mock.Mocker()
    def test_get_minutely_forecast_reloads_and_returns_data_block_object(self, mock):
        mock.get(requests_mock.ANY, json=self.json_data)
        self.assertIsInstance(self.forecast.minutely, ForecastioDataBlock)

    @requests_mock.Mocker()
    def test_get_hourly_forecast_reloads_and_returns_data_block_object(self, mock):
        mock.get(requests_mock.ANY, json=self.json_data)
        self.assertIsInstance(self.forecast.hourly, ForecastioDataBlock)

    @requests_mock.Mocker()
    def test_get_daily_forecast_reloads_and_returns_data_block_object(self, mock):
        mock.get(requests_mock.ANY, json=self.json_data)
        self.assertIsInstance(self.forecast.daily, ForecastioDataBlock)

    @requests_mock.Mocker()
    def test_get_currently_forecast_reloads_empty_and_returns_data_point_object(self, mock):
        mock.get(requests_mock.ANY, json={})
        self.assertIsInstance(self.forecast.currently, ForecastioDataPoint)

    @requests_mock.Mocker()
    def test_get_minutely_forecast_reloads_empty_and_returns_data_block_object(self, mock):
        mock.get(requests_mock.ANY, json={})
        self.assertIsInstance(self.forecast.minutely, ForecastioDataBlock)

    @requests_mock.Mocker()
    def test_get_hourly_forecast_reloads_empty_and_returns_data_block_object(self, mock):
        mock.get(requests_mock.ANY, json={})
        self.assertIsInstance(self.forecast.hourly, ForecastioDataBlock)

    @requests_mock.Mocker()
    def test_get_daily_forecast_reloads_empty_and_returns_data_block_object(self, mock):
        mock.get(requests_mock.ANY, json={})
        self.assertIsInstance(self.forecast.daily, ForecastioDataBlock)
