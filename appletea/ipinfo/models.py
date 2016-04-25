"""IP information data object model.

Data object model for IP information API responses.
"""


class IpInfo(object):
    def __init__(self, data):
        self.json = data

    @property
    def ip(self):
        return self._data('ip')

    @property
    def city(self):
        return self._data('city')

    @property
    def region(self):
        return self._data('region')

    @property
    def country(self):
        return self._data('country')

    @property
    def loc(self):
        loc = self._data('loc')
        return tuple(loc.split(','))

    @property
    def postal(self):
        return self._data('postal')

    @property
    def org(self):
        return self._data('org')

    def _data(self, key):
        if key in self.json:
            return self.json[key]
        raise ValueError(
                'Property "%s" not valid' \
                ' or is not available for this IP address.' % key
            )
