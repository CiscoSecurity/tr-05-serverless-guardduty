from collections import Counter
from datetime import timedelta, datetime

from api.mapping import SEVERITY
from api.tiles.factory import ITile


class EventsPerDayTile(ITile):

    @property
    def _id(self):
        return "events_per_day"

    @property
    def _type(self):
        return "vertical_bar_chart"

    @property
    def _tags(self):
        return [self._id]

    @property
    def _title(self):
        return "Events grouped by severity per day"

    @property
    def _description(self):
        return (
            f"{self._title} tile shows "
            "quantity of events per day for the given period of time."
        )

    @property
    def _short_description(self):
        return f"{self._title} for given time period."

    @property
    def _periods(self):
        return {
            "last_7_days": 7,
            "last_30_days": 30
        }

    @staticmethod
    def _parse_date(date):
        return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').date()

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
        key = data[0]
        data = data[1]
        return {
            "key": key,
            "values": self._values(data),
            "label": key,
            "value": len(data)
        }

    def _date_list(self, period):
        base = datetime.today()
        days = self._periods[period]

        return [
            (base - timedelta(days=x)).date() for x in range(days)
        ]

    def _group_by_date(self, data, period):
        date_list = self._date_list(period)

        return [
            (
                x.strftime('%m/%d'),
                [
                    y for y in data
                    if self._parse_date(y.UpdatedAt) == x
                ]
            )
            for x in date_list
        ]

    def tile_data(self, findings, period):
        grouped_findings = self._group_by_date(findings, period)

        return {
                "keys": self._keys(findings),
                "key_type": "string",
                "data": [
                    self._data(data) for data in grouped_findings
                ],
                **self.tile_extra_data(period)
            }
