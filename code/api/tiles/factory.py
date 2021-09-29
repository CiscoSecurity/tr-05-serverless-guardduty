from abc import ABCMeta, abstractmethod
from datetime import timedelta, datetime

from api.errors import TRFormattedError


INVALID_TILE_ID = "Invalid tile id"
DEFAULT_PERIOD = "last_7_days"


class TileFactory:

    @staticmethod
    def get_tile(tile_id, period):

        for cls in ITile.__subclasses__():
            if cls.__call__().id == tile_id:
                return cls(period)
        raise TRFormattedError(400, INVALID_TILE_ID)

    @staticmethod
    def list_tiles():
        def tile(cls):
            return {
                "id": cls.id,
                "type": cls.type,
                "title": cls.title,
                "tags": cls.tags,
                "description": cls.description,
                "short_description": cls.short_description,
                "periods": list(cls.periods.keys()),
                "default_period": cls.default_period
            }
        return [tile(cls.__call__()) for cls in ITile.__subclasses__()]


class ITile(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, period):
        self.period = period

    def observed_time(self):
        delta = timedelta(days=self.periods[self.period])
        today = datetime.today()

        return {
            'start_time': (today - delta).isoformat(timespec='milliseconds'),
            'end_time': datetime.now().isoformat(timespec='milliseconds')
        }

    def valid_time(self):
        return ITile.observed_time(self)

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

    def tile_data(self):
        """Returns tile data."""
        return {
            "hide_legend": False,
            "cache_scope": "none",
            "observed_time": self.observed_time(),
            "valid_time": self.valid_time()
        }

    def criteria(self):
        """Returns tile filter criteria."""
        days = timedelta(self.periods[self.period])
        date = int((datetime.utcnow() - days).timestamp() * 1000)

        return {
            "Criterion": {
                "updatedAt": {
                    "Gt": date,
                }
            }
        }
