"""Forecast data object model.

Data object model for Forecast API responses.
"""
import datetime
import requests


class Forecast(object):
    """Forecast data object.

    Forecast data can include 'current', 'minute-by-minute', 'hour-by-hour' or
    'day-by-day' weather information.

    Alerts contains any severe weather alerts, issued by a governmental weather
    authority, pertinent to the requested location.

    Flags is an object containing miscellaneous metadata concerning this
    request.
    """
    def __init__(self, json, response):
        self.response = response
        self.json = json

    @property
    def currently(self):
        """Return a data point containing the current weather conditions at the
        requested location.

        Returns:
          A ForecastioDataPoint object.
        """
        return self._data('currently')

    @property
    def minutely(self):
        """Return a data block containing the weather conditions
        minute-by-minute for the next hour.

        Returns:
          A ForecastioDataBlock object.
        """
        return self._data('minutely')

    @property
    def hourly(self):
        """Return a data block containing the weather conditions hour-by-hour
        for the next two days (or seven days if an extension was requested).

        Returns:
          A ForecastioDataBlock object.
        """
        return self._data('hourly')

    @property
    def daily(self):
        """Return a data block containing the weather conditions day-by-day for
        the next week.

        Returns:
          A ForecastioDataBlock object.
        """
        return self._data('daily')

    @property
    def alerts(self):
        """Return an object containing severe weather alerts.

        Returns:
          A list of Alert objects.
        """
        alerts = []
        for alertjson in self.json.get('alerts', []):
            alerts.append(Alert(alertjson))
        return alerts

    def _data(self, key):
        keys = ['minutely', 'currently', 'hourly', 'daily']
        try:
            if key not in self.json:
                keys.remove(key)
                args = {'exclude': '%s%s' % (','.join(keys), ',alerts,flags')}
                response = requests.get(
                    self.response.url.split('&')[0], params=args, timeout=5)
                response.raise_for_status()

                json_data = response.json()
                self.json[key] = json_data[key]

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
    """ForecastioDataBlock object.

    A data block object represents the various weather phenomena occurring over
    a period of time. Such objects contain the following properties:
      - summary: human-readable text summary of this data block.
      - icon: machine-readable text summary of this data block (see data point,
          for an enumeration of possible values that this property may take
          on).
      - data: list of data point objects (see above), ordered by time, which
          together describe the weather conditions at the requested location
          over time.

    Ideally, the minutely data block will contain data for the next hour, the
    hourly data block for the next two days, and the daily data block for the
    next week; however, if data for a given time period is lacking, the data
    point sequence may contain gaps or terminate early. Furthermore, if no data
    points for a time period are known, then the data block will be omitted
    from the response in its entirety. Developers are strongly encouraged,
    therefore, to check for the presence of data before attempting to read it.
    """
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
    """ForecastioDataPoint object.

    A data point object contains various properties, each representing a
    particular weather phenomenon occurring at a specific point in time. All of
    these properties (except time) are optional, and will only be set if that
    type of information for that location and time is available.

    Data points in the daily data block are special: instead of representing
    the weather phenomena at a given instant of time, they are an aggregate
    point representing (unless otherwise noted) the average weather conditions
    that will occur over the entire day.

    Data point objects may contain the following properties:
      - time: UNIX time (that is, seconds since midnight GMT on 1 Jan 1970) at
          which this data point occurs. 'minutely' data points are always
          aligned to the top of the minute, 'hourly' points to the top of the
          hour, and 'daily' points to midnight of the day, all according to the
          local time zone.
      - summary: human-readable text summary of this data point.
      - icon:machine-readable text summary of this data point, suitable for
          selecting an icon for display. If defined, this property will have
          one of the following values: 'clear-day', 'clear-night', 'rain',
          'snow', 'sleet', 'wind', 'fog', 'cloudy', 'partly-cloudy-day', or
          'partly-cloudy-night'. (Developers should ensure that a sensible
          default is defined, as additional values, such as 'hail',
          'thunderstorm', or 'tornado', may be defined in the future.)
      - sunriseTime/sunsetTime (only defined on daily data points): UNIX time
          (that is, seconds since midnight GMT on 1 Jan 1970) of the last
          sunrise before and first sunset after the solar noon closest to local
          noon on the given day.
      - moonPhase (only defined on daily data points): number representing the
          fractional part of the lunation number of the given day: a value of 0
          corresponds to a new moon, 0.25 to a first quarter moon, 0.5 to a
          full moon, and 0.75 to a last quarter moon. (The ranges in between
          these represent waxing crescent, waxing gibbous, waning gibbous, and
          waning crescent moons, respectively.)
      - nearestStormDistance (only defined on currently data points): numerical
          value representing the distance to the nearest storm in miles. (This
          value is very approximate and should not be used in scenarios
          requiring accurate results. In particular, a storm distance of zero
          does not necessarily refer to a storm at the requested location, but
          rather a storm in the vicinity of that location.)
      - nearestStormBearing (only defined on currently data points): numerical
          value representing the direction of the nearest storm in degrees,
          with true north at 0 degrees and progressing clockwise.
          (If nearestStormDistance is zero, then this value will not be
          defined. The caveats that apply to nearestStormDistance also apply to
          this value.)
      - precipIntensity: numerical value representing the average expected
          intensity (in inches/millimeters of liquid water per hour) of
          precipitation occurring at the given time conditional on probability
          (that is, assuming any precipitation occurs at all). A very rough
          guide is that a value of 0 in./hr. corresponds to no precipitation,
          0.002 in./hr. corresponds to very light precipitation, 0.017 in./hr.
          corresponds to light precipitation, 0.1 in./hr. corresponds to
          moderate precipitation, and 0.4 in./hr. corresponds to heavy
          precipitation.
      - precipIntensityMax, precipIntensityMaxTime (only defined on daily data
          points): numerical values representing the maximumum expected
          intensity of precipitation (and the UNIX time at which it occurs) on
          the given day in inches/millimeters of liquid water per hour.
      - precipProbability: numerical value between 0 and 1 (inclusive)
          representing the probability of precipitation occurring at the given
          time.
      - precipType: string representing the type of precipitation occurring at
          the given time. If defined, this property will have one of the
          following values: 'rain', 'snow', 'sleet' (which applies to each of
          freezing rain, ice pellets, and wintery mix), or 'hail'. (If
          precipIntensity is zero, then this property will not be defined.)
      - precipAccumulation (only defined on hourly and daily data points): the
          amount of snowfall accumulation expected to occur on the given day,
          in inches/centimeters. (If no accumulation is expected, this property
          will not be defined.)
      - temperature (not defined on daily data points): numerical value
          representing the temperature at the given time in degrees
          Fahrenheit/Celsius.
      - temperatureMin, temperatureMinTime, temperatureMax, and
          temperatureMaxTime (only defined on daily data points): numerical
          values representing the minimum and maximumum temperatures (and the
          UNIX times at which they occur) on the given day in degrees
          Fahrenheit/Celsius.
      - apparentTemperature (not defined on daily data points): numerical value
          representing the apparent (or "feels like") temperature at the given
          time in degrees Fahrenheit/Celsius.
      - apparentTemperatureMin, apparentTemperatureMinTime,
          apparentTemperatureMax, and apparentTemperatureMaxTime (only defined
          on daily data points): numerical values representing the minimum and
          maximumum apparent temperatures (and the UNIX times at which they
          occur) on the given day in degrees Fahrenheit/Celsius.
      - dewPoint: numerical value representing the dew point at the given time
          in degrees Fahrenheit/Celsius.
      - windSpeed: numerical value representing the wind speed in miles/meters
          per hour/second.
      - windBearing: numerical value representing the direction that the wind
          is coming from in degrees, with true north at 0 degrees and
          progressing clockwise. (If windSpeed is zero, then this value will
          not be defined.)
      - cloudCover: numerical value between 0 and 1 (inclusive) representing
          the percentage of sky occluded by clouds.
      - humidity: numerical value between 0 and 1 (inclusive) representing the
          relative humidity.
      - pressure: numerical value representing the sea-level air pressure in
          millibars/hectopascals.
      - visibility: numerical value representing the average visibility in
          miles/kilometers, capped at 10 miles/kilometers.
      - ozone: numerical value representing the columnar density of total
          atmospheric ozone at the given time in Dobson units.
    """
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
    """Alert data object.

    An alert data object represents a severe weather warning issued for the
    requested location by a governmental authority. Alert objects contain the
    following properties:
      - title: short text summary of the alert.
      - expires: UNIX time (that is, seconds since midnight GMT on 1 Jan 1970)
          at which the alert will cease to be valid.
      - description: detailed text description of the alert from the
          appropriate weather service.
      - uri: HTTP(S) URI that contains detailed information about the alert.
    """
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
