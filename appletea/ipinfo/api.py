"""Client for ipinfo.io APIs.

A REST client library for ipinfo.io APIs.
"""
import json
import requests

from appletea.ipinfo.models import IpInfo


def get_ipinfo(ip='', param='json'):
    """Return IP information.

    Return an IP information object. You can pass in the IP you are interested
    in, or omit it to get details about your own IP. If you are only interested
    in specific details you can pass param to get a plain text response that
    includes just the parameter you are after. You can specify 'loc' to get
    just the geolocation information, which will often be faster than getting
    the full response.

    Args:
      ip: locally bound IP address if omitted.
      param: optional argument can be 'ip', 'hostname', 'city', 'region',
      'country', 'loc', 'org' or 'postal'.

    Returns:
      An IP information object with methods for accessing its data. Raises a
      request.HTTPError when a bad request is made (a 4xx client error
      or 5xx server error response).
    """
    if ip:
        urlpart = '%s/%s' % (ip, param)
    else:
        urlpart = param

    response = requests.get('http://ipinfo.io/%s' % urlpart, timeout=5)
    response.raise_for_status()

    if param == 'json':
        data = response.json()
    else:
        data = json.dumps({param: response.text.strip()})

    return IpInfo(data)
