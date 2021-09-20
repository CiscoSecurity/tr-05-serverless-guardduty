from datetime import datetime, timedelta

from api.charts.factory import IChart


class AffectedInstances(IChart):
    PERIODS = {
        "last_24_hours": 1,
        "last_7_days": 7,
        "last_30_days": 30
    }

    def criterion(self, period):
        date_format = "%d-%m-%Y"
        date = (datetime.now().date() - timedelta(self.PERIODS[period]))
        date = date.strftime(date_format)
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

    @staticmethod
    def id():
        return "affected_instances"

    @staticmethod
    def affected_iscs_id(findings):
        return list(
            set(
                [
                    finding.resource.details.instance_id for finding
                    in findings
                ]
            )
        )

    @staticmethod
    def finding_types(findings):
        return list(
            set(
                [finding.type for finding in findings]
            )
        )

    @staticmethod
    def _sum_of_findings_by_isc(instance, findings):
        return sum(
            finding.resource.details.instance_id == instance for finding
            in findings
        )

    def _segments(self, instance, findings):
        def segment(_type):
            return {
                "key": self.finding_types(findings).index(_type),
                "value": sum(
                    finding.type == _type and
                    finding.resource.details.instance_id == instance
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
