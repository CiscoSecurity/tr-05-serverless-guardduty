from abc import ABCMeta, abstractmethod
from api.errors import TRFormattedError


INVALID_CHART_ID = "Invalid chart id"


class ChartFactory:

    @staticmethod
    def get_chart(chart_id):
        for cls in IChart.__subclasses__():
            if cls.id() == chart_id:
                return cls()
        raise TRFormattedError(400, INVALID_CHART_ID)


class IChart(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def id():
        """Returns id of specific type of chart."""

    @staticmethod
    @abstractmethod
    def criterion(self):
        """Returns filter criterion for specific type of chart."""

    @abstractmethod
    def build(self, findings):
        """Returns structure for specific type of chart."""
