from typing import Optional
from abc import ABCMeta, abstractmethod


class Observable(metaclass=ABCMeta):
    """An observable to search records for."""

    @staticmethod
    def of(type_: str) -> Optional['Observable']:
        """Returns an instance of `Observable` for the specified type."""

        for cls in Observable.__subclasses__():
            if cls.type() == type_:
                return cls()

        return None

    @staticmethod
    @abstractmethod
    def type() -> str:
        """Returns the observable type."""

    @abstractmethod
    def query(self, observable: str) -> dict:
        """Returns criterion."""


class IP(Observable):

    @staticmethod
    def type() -> str:
        return 'ip'

    def query(self, observable: str) -> dict:
        return {
            "Criterion": {
                "resource.instanceDetails.networkInterfaces.publicIp": {
                    "Equals": [
                        observable
                    ]
                }
            }
        }


class IPV6(Observable):

    @staticmethod
    def type() -> str:
        return 'ipv6'

    def query(self, observable: str) -> dict:
        return {
            "Criterion": {
                "resource.instanceDetails.networkInterfaces.ipv6Addresses": {
                    "Equals": [
                        observable
                    ]
                }
            }
        }
