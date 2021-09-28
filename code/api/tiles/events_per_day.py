from collections import Counter
from datetime import timedelta, datetime

from api.mapping import SEVERITY
from api.tiles.factory import ITile, DEFAULT_PERIOD


class EventsPerDay(ITile):
    def __init__(self, period=DEFAULT_PERIOD):
        self._type = "vertical_bar_chart"
        self._id = "events_per_day"
        self._title = "Events grouped by severity per day"
        self._tags = [
            "events_per_day"
        ]
        self._periods = {
            "last_24_hours": 1,
            "last_7_days": 7,
            "last_30_days": 30
        }
        self.period = period
        self._description = (
            "Events grouped by severity per day chart shows "
            "quantity of events per day for the given period of time."
        )
        self._short_description = ("Events grouped by severity per day "
                                   "for given time period.")

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def tags(self):
        return self._tags

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def short_description(self):
        return self._short_description

    @property
    def periods(self):
        return self._periods

    @staticmethod
    def _convert_date(date):
        return datetime.strptime(date.split("T")[0], '%Y-%m-%d')

    @staticmethod
    def _keys(data):
        def key(item):
            item = SEVERITY[int(item.Severity)]
            return {
                "key": item.lower(),
                "label": item
            }

        keys = [key(item) for item in data]
        return list({v['key']: v for v in keys}.values())

    @staticmethod
    def _values(data):
        severity_count = Counter(
            [SEVERITY[int(item.Severity)] for item in data]
        )

        return [
            {
                "key": item[0].lower(),
                "value": item[1]
            } for item in severity_count.items()
        ]

    def _data(self, data):
        key = list(data.keys())[0]
        data = list(data.values())[0]
        return {
            "key": key,
            "values": self._values(data),
            "label": key,
            "value": len(data)
        }

    def _group_by_date(self, data):
        base = datetime.today()
        days = self.periods[self.period]
        date_list = [
            (base - timedelta(days=x)).date() for x in range(days)
        ]

        return [
            {
                str(x): [
                    y for y in data
                    if self._convert_date(y.UpdatedAt).date() == x
                ]
            }
            for x in date_list
        ]

    def tile_data(self, findings):
        build = super(EventsPerDay, self).tile_data()

        grouped_findings = self._group_by_date(findings)
        build.update(
            {
                "keys": self._keys(findings),
                "key_type": "string",
                "data": [
                    self._data(data) for data in grouped_findings
                    if list(data.values())[0]
                ]
            }
        )
        return build
