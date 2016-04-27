"""IP address location data object model.

Data object model for IP information API responses.
"""


class IpInfo(object):
    """Ip address location object.

    IP address location data can include information such as city, region,
    country, latitude, longitude, organisation or postal/zip code. Its
    constructor takes JSON-formatted data.
    """
    def __init__(self, json):
        self.json = json

    @property
    def loc(self):
        """Return location information.

        Returns:
          A tuple of geographic latitude and longitude coordinates in decimal
          degrees.
        """
        location = self.__getattr__('loc')
        return tuple(location.split(','))

    def __getattr__(self, name):
        try:
            return self.json[name]
        except KeyError:
            raise ValueError(
                'Property "%s" not valid'
                ' or is not available for this IP address.' % name
            )
