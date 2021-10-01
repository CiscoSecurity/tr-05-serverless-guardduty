from api.tiles.factory import ITile


FINDING_TYPES = dict(Instance="EC2", AccessKey="IAM", S3Bucket="S3")


class TotalEventsTile(ITile):
    @property
    def _id(self):
        return "total_events"

    @property
    def _type(self):
        return "metric_group"

    @property
    def _tags(self):
        return [self._id]

    @property
    def _title(self):
        return "Total Events"

    @property
    def _description(self):
        return (
            f"{self._title} tile provides "
            f"the total number of findings"
            f" grouped by resource type."
        )

    @property
    def _short_description(self):
        return self._description

    @property
    def _periods(self):
        return {
            "last_24_hours": 1,
            "last_7_days": 7,
            "last_30_days": 30,
            "last_60_days": 60,
            "last_90_days": 90
        }

    @staticmethod
    def _data(findings):
        def metric(_type):
            data = filter(lambda f: f.Resource.ResourceType == _type, findings)
            return {
                "icon": "warning",
                "label": f"{FINDING_TYPES[_type]} finding types",
                "value": sum([finding.Service.Count for finding in data]),
                "value_unit": "integer",
            }
        return [metric(_type) for _type in FINDING_TYPES.keys()]

    def tile_data(self, findings, period):
        return {
            "data": self._data(findings),
            **self.tile_extra_data(period)
        }
