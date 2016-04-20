"""
The Forecast API allows you to look up the weather anywhere on the globe,
returning (where available):

- Current conditions
- Minute-by-minute forecasts out to 1 hour
- Hour-by-hour forecasts out to 48 hours
- Day-by-day forecasts out to 7 days

More information: https://developer.forecast.io
"""
from api import get_forecast


__all__ = ['get_forecast']