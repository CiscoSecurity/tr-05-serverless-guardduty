from abc import ABCMeta, abstractmethod
from api.errors import TRFormattedError


INVALID_CHART_ID = "Invalid chart id"


class ChartFactory:

    @staticmethod
    def chart(chart_id):
        for cls in IChart.__subclasses__():
            if cls.id() == chart_id:
                return cls()
        raise TRFormattedError(400, INVALID_CHART_ID)


class IChart(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def id():
        """Returns id of specific type of chart."""

    @abstractmethod
    def criterion(self):
        """Returns filter criterion for specific type of chart."""

    @abstractmethod
    def build(self, findings):
        """Returns structure for specific type of chart."""


class AffectedInstances(IChart):

    @property
    def criterion(self):
        return {
            "Criterion": {
                "resource.resourceType": {
                    "Equals": [
                        "Instance"
                    ]
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
                [finding.resource.details.instance_id for finding in findings]
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
            finding.resource.details.instance_id == instance for finding in
            findings
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
            "labels": [
                self.affected_iscs_id(findings), self.finding_types(findings)
            ],
            "data": [
                self._data(instance, findings) for instance
                in self.affected_iscs_id(findings)
            ]
        }
