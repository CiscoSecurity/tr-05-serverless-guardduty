from typing import Optional
from abc import ABCMeta, abstractmethod

from flask import current_app


IP_ATTRS = [
    "resource.instanceDetails.networkInterfaces.publicIp",
    "service.action.awsApiCallAction.remoteIpDetails.ipAddressV4",
    "service.action.networkConnectionAction.localIpDetails.ipAddressV4",
    "service.action.networkConnectionAction.remoteIpDetails.ipAddressV4",
    "resource.instanceDetails.networkInterfaces.privateIpAddresses"
    ".privateIpAddress"
]

IPV6_ATTRS = [
    "resource.instanceDetails.networkInterfaces.ipv6Addresses"
]


class Observable(metaclass=ABCMeta):
    """An observable to search records for."""

    @staticmethod
    def criterion(attribute: str, observable: str, condition: str = 'Equals'):
        return {
            "Criterion": {
                attribute: {
                    condition: [
                        observable
                    ]
                }
            }
        }

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
        """Returns criteria."""

    @staticmethod
    def refer(value: str, type_: str) -> dict:
        """Build an GuardDuty reference for the current observable."""
        url = current_app.config['GUARD_DUTY_REFER_URL']
        types = {
            'ip': 'IP',
            'ipv6': 'IPv6'
        }
        human_readable_type_ = types[type_]
        return {
            'id': f'ref-aws-detective-search-{type_}-{value}',
            'title': f'Search for this {human_readable_type_}',
            'description': f'Check this {human_readable_type_} '
                           f'with Amazon Detective',
            'url': url.format(region=current_app.config['AWS_REGION'],
                              observable=value),
            'categories': ['Search', 'Amazon Detective'],
        }


class IP(Observable):

    @staticmethod
    def type() -> str:
        return 'ip'

    def query(self, observable: str) -> list:
        return [
            self.criterion(attribute, observable) for attribute in IP_ATTRS
        ]


class IPv6(Observable):

    @staticmethod
    def type() -> str:
        return 'ipv6'

    def query(self, observable: str) -> list:
        return [
            self.criterion(attribute, observable) for attribute in IPV6_ATTRS
        ]
