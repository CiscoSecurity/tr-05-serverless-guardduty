from datetime import datetime, timedelta

from api.charts.factory import IChart


class AffectedInstances(IChart):

    def __init__(self):
        self._type = "donut_graph"
        self._id = "affected_instances"
        self._title = "Affected instances"
        self._periods = {
            "last_24_hours": 1,
            "last_7_days": 7,
            "last_30_days": 30
        }
        self._default_period = "last_7_days"
        self._description = (
            "Affected Instances chart shows "
            "what types of findings EC2 instances have."
        )

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def periods(self):
        return self._periods

    @property
    def default_period(self):
        return self._default_period

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
            set(
                [finding.Type for finding in findings]
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

    def criterion(self, period):
        date_format = "%d-%m-%Y"
        days = timedelta(self.periods.get(period, self.default_period))
        date = (datetime.now().date() - days).strftime(date_format)
        date = int(datetime.strptime(date, date_format).strftime("%s"))

        return {
            "Criterion": {
                "resource.resourceType": {
                    "Equals": [
                        "Instance"
                    ]
                },
                "updatedAt": {
                    "Gt": date,
                }
            }
        }

    def build(self, findings):
        return {
            "hide_legend": False,
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
