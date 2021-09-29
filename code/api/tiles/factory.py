from abc import ABCMeta, abstractmethod
from datetime import timedelta, datetime

from api.errors import TRFormattedError


INVALID_TILE_ID = "Invalid tile id"
DEFAULT_PERIOD = "last_7_days"


class TileFactory:

    @staticmethod
    def get_tile(tile_id):

        for cls in ITile.__subclasses__():
            if cls.__call__().id == tile_id:
                return cls()
        raise TRFormattedError(400, INVALID_TILE_ID)

    @staticmethod
    def list_tiles():
        return [cls().tile() for cls in ITile.__subclasses__()]


class ITile(metaclass=ABCMeta):

    def observed_time(self, period):
        delta = timedelta(days=self.periods[period])
        today = datetime.today()

        return {
            'start_time': (today - delta).isoformat(timespec='milliseconds'),
            'end_time': datetime.now().isoformat(timespec='milliseconds')
        }

    def valid_time(self, period):
        return self.observed_time(period)

    @property
    @abstractmethod
    def id(self):
        """Returns tile id."""

    @property
    @abstractmethod
    def type(self):
        """Returns tile type."""

    @property
    @abstractmethod
    def tags(self):
        """Returns tile tags."""

    @property
    @abstractmethod
    def title(self):
        """Returns tile title."""

    @property
    @abstractmethod
    def description(self):
        """Returns tile description."""

    @property
    @abstractmethod
    def short_description(self):
        """Returns tile short description."""

    @property
    @abstractmethod
    def periods(self):
        """Returns tile available periods to represent data."""

    @property
    def default_period(self):
        """Returns tile default period."""
        return DEFAULT_PERIOD

    def criteria(self, period):
        """Returns tile filter criteria."""
        days = timedelta(self.periods[period])
        date = int((datetime.utcnow() - days).timestamp() * 1000)

        return {
            "Criterion": {
                "updatedAt": {
                    "Gt": date,
                }
            }
        }

    def tile_data(self, period):
        """Returns tile data."""
        return {
            "hide_legend": False,
            "cache_scope": "none",
            "observed_time": self.observed_time(period),
            "valid_time": self.valid_time(period)
        }

    def tile(self):
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "tags": self.tags,
            "description": self.description,
            "short_description": self.short_description,
            "periods": list(self.periods.keys()),
            "default_period": self.default_period
        }
