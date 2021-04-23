from flask import current_app
from abc import ABCMeta, abstractmethod
from typing import Optional, Dict, Union, List


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

    @staticmethod
    def refer(value: str) -> dict:
        """Build an GuardDuty reference for the current observable."""
        url = current_app.config['GUARD_DUTY_REFER_URL']
        return {
            'id': f'ref-aws-detective-search-ip-{value}',
            'title': 'Search for this IP',
            'description': 'Check this IP with AWS Detective',
            'url': url.format(region=current_app.config['AWS_REGION'],
                              observable=value),
            'categories': ['Search', 'AWS Detective'],
        }


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
