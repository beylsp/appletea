"""Client for forecast.io APIs.

A REST client library for forecast.io APIs.
"""
import requests

from forecastio.models import Forecast


def get_forecast(key, latitude, longitude, **kwargs):
    """Return weather forecast for a given location.

    Return a weather forecast object for a given location. The key should be
    your Dark Sky API key, latitude and longitude should be the geographic
    coordinates of a location in decimal degrees. Additional arguments can be:
      - units=[setting]: return the API response in units rather than the
          default Imperial units. Following settings are possible: 'us', 'si',
          'ca', 'uk2' or 'auto'.
      - exclude=[blocks]: exclude some number of data blocks from the API
          response useful for reducing latency and cache space. [blocks]
          should be a comma-delimited list (without spaces) of any of the
          following: 'currently', 'minutely', 'hourly', 'daily', 'alerts',
          'flags'.
      - extend=hourly: return hourly data for the next seven days, rather then
          than next two.
      - lang=[language]: return summary properties in the desired language.

    Args:
      key: Dark Sky API key.
      latitude: geographic latitude coordinates in decimal degrees.
      longitude: geographic longitude coordinated in decimal degrees.
      kwargs: additional arguments passed to requests.get.

    Returns:
      A Forecast object with methods for accessing its data.
    """
    response = requests.get('https://api.forecast.io/forecast/%s/%s,%s' %
                            (key, latitude, longitude), params=kwargs)
    response.raise_for_status()

    json = response.json()
    headers = response.headers

    return Forecast(json, response, headers)
