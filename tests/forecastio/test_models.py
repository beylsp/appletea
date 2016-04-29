import json
import os.path as osp
import requests
import requests_mock
import unittest

from appletea.forecastio.models import (
    Forecast, ForecastioDataPoint, ForecastioDataBlock)


class TestModels(unittest.TestCase):
    def setUp(self):
        response = requests.Response()
        json_file = osp.join(
            osp.dirname(osp.abspath(__file__)), 'data/test.json')
        with open(json_file) as fp:
            self.json_data = json.loads(fp.read())
        self.forecast = Forecast(self.json_data, response)

    def test_get_currently_forecast_returns_data_point_object(self):
        self.assertIsInstance(self.forecast.currently, ForecastioDataPoint)

    def test_get_minutely_forecast_returns_data_block_object(self):
        self.assertIsInstance(self.forecast.minutely, ForecastioDataBlock)

    def test_get_hourly_forecast_returns_data_block_object(self):
        self.assertIsInstance(self.forecast.hourly, ForecastioDataBlock)

    def test_get_daily_forecast_returns_data_block_object(self):
        self.assertIsInstance(self.forecast.daily, ForecastioDataBlock)

    def test_get_alerts_forecast_returns_alert_object_list(self):
        self.assertIsInstance(self.forecast.alerts, list)


class TestModelsEmptyData(unittest.TestCase):
    def setUp(self):
        json_file = osp.join(
            osp.dirname(osp.abspath(__file__)), 'data/test.json')
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
