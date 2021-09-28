from api.tiles.factory import ITile, DEFAULT_PERIOD


class AffectedInstances(ITile):

    def __init__(self, period=DEFAULT_PERIOD):
        self._type = "donut_graph"
        self._id = "affected_instances"
        self._title = "Affected instances"
        self._tags = [
            "affected_instances"
        ]
        self._periods = {
            "last_24_hours": 1,
            "last_7_days": 7,
            "last_30_days": 30
        }
        self.period = period
        self._description = (
            "Affected Instances chart shows "
            "what types of findings EC2 instances have."
        )
        self._short_description = ("Affected Instances by finding types "
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
    def affected_iscs_id(findings):
        return list(
            set(
                [
                    finding.Resource.InstanceDetails.InstanceId for finding
                    in findings
                ]
            )
        )

    @staticmethod
    def finding_types(findings):
        return list(
            sorted(
                set(
                    [finding.Type for finding in findings]
                )
            )
        )

    @staticmethod
    def _sum_of_findings_by_isc(instance, findings):
        return sum(
            finding.Resource.InstanceDetails.InstanceId == instance for finding
            in findings
        )

    def _segments(self, instance, findings):
        def segment(_type):
            return {
                "key": self.finding_types(findings).index(_type),
                "value": sum(
                    finding.Type == _type and
                    finding.Resource.InstanceDetails.InstanceId == instance
                    for finding in findings
                )
            }

        return [segment(_type) for _type in self.finding_types(findings)]

    def _data(self, instance, findings):
        return {
            "key": self.affected_iscs_id(findings).index(instance),
            "value": self._sum_of_findings_by_isc(instance, findings),
            "segments": self._segments(instance, findings)
        }

    def criteria(self):
        criterion = super(AffectedInstances, self).criteria()
        criterion["Criterion"].update(
            {
                "resource.resourceType": {
                    "Equals": [
                        "Instance"
                    ]
                }
            }
        )
        return criterion

    def tile_data(self, findings):
        build = super(AffectedInstances, self).tile_data()
        build.update(
            {
                "label_headers": [
                    "Affected instances",
                    "Finding types"
                ],
                "labels": [
                    self.affected_iscs_id(findings),
                    self.finding_types(findings)
                ],
                "data": [
                    self._data(instance, findings) for instance
                    in self.affected_iscs_id(findings)
                ]
            }
        )
        return build
