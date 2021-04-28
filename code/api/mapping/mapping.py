from flask import current_app
from api.utils import RangeDict
from .sighting import Sighting
from .indicator import Indicator
from bundlebuilder.models import Observable


class Mapping:

    SIGHTING = 'sighting'
    CONFIDENCE = 'High'

    SOURCE_URI = \
        'https://console.aws.amazon.com/guardduty/home?' \
        '{region}/findings&region={region}#/findings?' \
        'macros=current&fId={finding_id}'

    SEVERITY = RangeDict({
        range(7, 9): 'High',
        range(4, 7): 'Medium',
        range(1, 4): 'Low'
    })

    SENSOR = 'network.ips'
    SOURCE = 'AWS GuardDuty findings'

    DEFAULTS = {
        'confidence': CONFIDENCE,
        'source': SOURCE
    }

    NETWORK_CONNECTION = 'NETWORK_CONNECTION'
    PORT_PROBE = 'PORT_PROBE'
    DNS_REQUEST = 'DNS_REQUEST'
    AWS_API_CALL = 'AWS_API_CALL'

    def __init__(self, type_, value, data):
        self.observable = Observable(
            type=type_,
            value=value
        )
        self.aws_region = current_app.config['AWS_REGION']
        self.data = data
        self._sighting = Sighting(self)
        self._indicator = Indicator(self)

    def get_sighting(self):
        return self._sighting.extract()

    def get_indicator(self):
        return self._indicator.extract()

    def service(self):
        return self.data['Service']

    def severity(self):
        return self.SEVERITY[int(self.data['Severity'])]

    def action(self):
        return self.service()['Action']

    def action_type(self):
        return self.action()['ActionType']

    def source_uri(self):
        return self.SOURCE_URI.format(
            region=self.aws_region, finding_id=self.data['Id']
        )

    def action_data(self, type_):
        actions = {
            self.DNS_REQUEST: lambda d: d['DnsRequestAction'],
            self.AWS_API_CALL: lambda d: d['AwsApiCallAction'],
            self.NETWORK_CONNECTION: lambda d: d['NetworkConnectionAction'],
            self.PORT_PROBE: lambda d: d['PortProbeAction']['PortProbeDetails']
        }
        return actions[type_](self.action())
