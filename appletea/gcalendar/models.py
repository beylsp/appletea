from appletea.utils import UnicodeMixin


class GCalendarEvents(UnicodeMixin):
    def __init__(self, json):
        self.json = json
        self.events = [GEventData(item) for item in json.get('items', [])]

    def __unicode__(self):
        return ('<GCalendarEvents instance with %d events>' % len(self.events))


class GEventData(UnicodeMixin):
    def __init__(self, d={}, supitem=''):
        self.supitem = supitem
        self.d = d

    def __getattr__(self, name):
        try:
            v = self.d[name]
            if isinstance(v, dict):
                return GEventData(v, name)
            elif isinstance(v, list):
                return map(lambda x: GEventData(x, name), v)
            else:
                return v
        except KeyError:
            raise ValueError(
                'Property "%s" not valid or is not available for event'
                ' %s.' % (name, 
                         'item "%s"' % self.supitem if self.supitem else 'item')
            )

    def __unicode__(self):
        return ('<GEventData instance: %s>' % self.supitem)
