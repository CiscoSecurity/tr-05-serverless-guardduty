from abc import ABCMeta, abstractmethod
from datetime import timedelta, datetime

from api.errors import TRFormattedError
from api.client import GuardDuty

INVALID_TILE_ID = "Invalid tile id"
DEFAULT_PERIOD = "last_7_days"


def all_subclasses(cls):
    return set(cls.__subclasses__())\
        .union([s for c in cls.__subclasses__() for s in all_subclasses(c)])


class TileFactory:

    @staticmethod
    def get_tile(tile_id):

        for cls in all_subclasses(ITile):
            if cls()._id == tile_id:
                return cls()
        raise TRFormattedError(400, INVALID_TILE_ID)

    @staticmethod
    def list_tiles():
        return [cls().tile() for cls in all_subclasses(ITile)]


class ITile(metaclass=ABCMeta):

    def observed_time(self, period):
        delta = timedelta(days=self._periods[period])
        today = datetime.today()

        return {
            'start_time': (today - delta).isoformat(timespec='milliseconds'),
            'end_time': datetime.now().isoformat(timespec='milliseconds')
        }

    def valid_time(self, period):
        return self.observed_time(period)

    @property
    @abstractmethod
    def _id(self):
        """Returns tile id."""

    @property
    @abstractmethod
    def _type(self):
        """Returns tile type."""

    @property
    @abstractmethod
    def _tags(self):
        """Returns tile tags."""

    @property
    @abstractmethod
    def _title(self):
        """Returns tile title."""

    @property
    @abstractmethod
    def _description(self):
        """Returns tile description."""

    @property
    @abstractmethod
    def _short_description(self):
        """Returns tile short description."""

    @property
    @abstractmethod
    def _periods(self):
        """Returns tile available periods to represent data."""

    @property
    def _default_period(self):
        """Returns tile default period."""
        return DEFAULT_PERIOD

    @property
    def limit(self):
        return 0

    @property
    def sort_criteria(self):
        """Returns sorting criteria."""
        return GuardDuty.DEFAULT_ORDER

    @abstractmethod
    def tile_data(self):
        """Returns tile mapped data."""

    def finding_criteria(self, period):
        """Returns tile filter criteria."""
        days = timedelta(self._periods[period])
        date = int((datetime.utcnow() - days).timestamp() * 1000)

        return {
            "Criterion": {
                "updatedAt": {
                    "Gt": date,
                }
            }
        }

    def tile_extra_data(self, period):
        """Returns tile extra data."""
        return {
            "hide_legend": False,
            "cache_scope": "none",
            "observed_time": self.observed_time(period),
            "valid_time": self.valid_time(period)
        }

    def tile(self):
        """Returns tile object."""
        return {
            "id": self._id,
            "type": self._type,
            "title": self._title,
            "tags": self._tags,
            "description": self._description,
            "short_description": self._short_description,
            "periods": list(self._periods.keys()),
            "default_period": self._default_period
        }
