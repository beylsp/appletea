"""Forecast data object model.

Data object model for Forecast API responses.
"""
import datetime
import requests


class Forecast(object):
    def __init__(self, data, response):
        self.response = response
        self.json = data

        self._alerts = []
        for alertjson in self.json.get('alerts', []):
            self._alerts.append(Alert(alertjson))

    def currently(self):
        return self._data('currently')

    def daily(self):
        return self._data('daily')

    def _data(self, key):
        keys = ['minutely', 'currently', 'hourly', 'daily']
        try:
            if key not in self.json:
                keys.remove(key)
                response = requests.get(
                    self.response.url.split('&')[0],
                    exclude='%s%s' % (','.join(keys), ',alerts,flags')
                ).json()
                self.json[key] = response[key]

            if key == 'currently':
                return ForecastioDataPoint(self.json[key])
            else:
                return ForecastioDataBlock(self.json[key])
        except:
            if key == 'currently':
                return ForecastioDataPoint()
            else:
                return ForecastioDataBlock()


class ForecastioDataBlock(object):
    def __init__(self, d=None):
        d = d or {}
        self.summary = d.get('summary')
        self.icon = d.get('icon')

        self.data = [ForecastioDataPoint(datapoint)
                     for datapoint in d.get('data', [])]

    def __unicode__(self):
        return '<ForecastioDataBlock instance:' \
               ' %s with %d ForecastioDataPoints>' % (self.summary,
                                                      len(self.data))


class ForecastioDataPoint(object):
    def __init__(self, d={}):
        self.d = d

        try:
            self.time = datetime.datetime.utcfromtimestamp(int(d['time']))
            self.utime = d['time']
        except:
            self.time = None
            self.utime = None

        try:
            sr_time = int(d['sunriseTime'])
            self.sunrise_time = datetime.datetime.utcfromtimestamp(sr_time)
        except:
            self.sunrise_time = None

        try:
            ss_time = int(d['sunsetTime'])
            self.sunset_time = datetime.datetime.utcfromtimestamp(ss_time)
        except:
            self.sunset_time = None

    def __getattr__(self, name):
        try:
            return self.d[name]
        except KeyError:
            raise ValueError(
                'Property "%s" not valid'
                ' or is not available for this forecast.' % name
            )

    def __unicode__(self):
        return ('<ForecastioDataPoint instance: '
                '%s at %s>' % (self.summary, self.time))


class Alert(object):
    def __init__(self, json):
        self.json = json

    def __getattr__(self, name):
        try:
            return self.json[name]
        except KeyError:
            raise ValueError(
                'Property "%s" not valid'
                ' or is not available for this forecast.' % name
            )

    def __unicode__(self):
        return '<Alert instance: %s at %s>' % (self.title, self.time)
