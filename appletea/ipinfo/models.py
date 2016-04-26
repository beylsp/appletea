"""IP information data object model.

Data object model for IP information API responses.
"""


class IpInfo(object):
    def __init__(self, json):
        self.json = json

    @property
    def loc(self):
        location = self.__getattr__('loc')
        return tuple(location.split(','))

    def __getattr__(self, name):
        try:
            return self.json[name]
        except KeyError:
            raise ValueError(
                'Property "%s" not valid' \
                ' or is not available for this IP address.' % name
            )
