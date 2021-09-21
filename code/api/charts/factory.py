from abc import ABCMeta, abstractmethod
from api.errors import TRFormattedError


INVALID_CHART_ID = "Invalid chart id"


class ChartFactory:

    @staticmethod
    def get_chart(chart_id):

        for cls in IChart.__subclasses__():
            if cls.__call__().id == chart_id:
                return cls()
        raise TRFormattedError(400, INVALID_CHART_ID)

    @staticmethod
    def list_charts():
        def chart(cls):
            return {
                "id": cls.id,
                "type": cls.type,
                "title": cls.title,
                "description": cls.description,
                "periods": cls.periods,
                "default_period": cls.default_period
            }
        return [chart(cls.__call__()) for cls in IChart.__subclasses__()]


class IChart(metaclass=ABCMeta):

    @property
    @abstractmethod
    def id(self):
        """Returns chart id."""

    @property
    @abstractmethod
    def type(self):
        """Returns chart type."""

    @property
    @abstractmethod
    def title(self):
        """Returns chart title."""

    @property
    @abstractmethod
    def description(self):
        """Returns chart description."""

    @property
    @abstractmethod
    def periods(self):
        """Returns chart available periods to represent data."""

    @staticmethod
    @abstractmethod
    def criterion(self):
        """Returns chart filter criteria."""

    @abstractmethod
    def build(self, findings):
        """Returns chart data."""
