from datetime import datetime
from flask import current_app
from typing import OrderedDict
from api.utils import RangeDict

from bundlebuilder.models import (
    ObservedRelation,
    Observable,
    Sighting,
    ObservedTime,
    IdentitySpecification
)

SOURCE = 'AWS GuardDuty findings'
SIGHTING = 'sighting'

SENSOR = 'network.ips'
SIGHTING_DEFAULTS = {
    'sensor': SENSOR,
    'confidence': 'High',
    'source': SOURCE
}

SOURCE_URI = \
    'https://console.aws.amazon.com/guardduty/home?' \
    '{region}/findings&region={region}#/findings?' \
    'macros=current&fId={finding_id}'

NETWORK_CONNECTION = 'NETWORK_CONNECTION'
PORT_PROBE = 'PORT_PROBE'
DNS_REQUEST = 'DNS_REQUEST'
AWS_API_CALL = 'AWS_API_CALL'

SEVERITY = RangeDict({
    range(7, 9): 'High',
    range(4, 7): 'Medium',
    range(1, 4): 'Low'
})


LOCAL_IP = 'LocalIpDetails'
REMOTE_IP = 'RemoteIpDetails'

DIRECTION = {
    'INBOUND': (REMOTE_IP, LOCAL_IP),
    'OUTBOUND': (LOCAL_IP, REMOTE_IP)
}


class Mapping:

    def __init__(self, type_, value):
        self.observable = Observable(
            type=type_,
            value=value
        )
        self.aws_region = current_app.config['AWS_REGION']
        self.sighting = self.Sighting(self)

    @staticmethod
    def ip(action, type_):
        return action[type_]['IpAddressV4']

    @staticmethod
    def service(data):
        return data['Service']

    def action(self, data):
        return self.service(data)['Action']

    def action_data(self, data, type_):
        actions = {
            DNS_REQUEST: lambda d: d['DnsRequestAction'],
            AWS_API_CALL: lambda d: d['AwsApiCallAction'],
            NETWORK_CONNECTION: lambda d: d['NetworkConnectionAction'],
            PORT_PROBE: lambda d: d['PortProbeAction']['PortProbeDetails']
        }
        return actions[type_](self.action(data))

    def action_type(self, data):
        return self.action(data)['ActionType']

    class Sighting:
        def __init__(self, root):
            self.root = root

        @staticmethod
        def observables(finding: OrderedDict):

            interfaces = \
                finding['Resource']['InstanceDetails']['NetworkInterfaces']

            def observable(type_, value):
                for data in interfaces:
                    if data.get(value, 'Unknown') != 'Unknown':
                        return Observable(type=type_, value=data[value])

            yield observable('ip', 'PublicIp')
            yield observable('domain', 'PublicDnsName')

        def _observed_time(self, finding):
            service = self.root.service(finding)
            start_date = service['EventFirstSeen']
            end_date = service['EventLastSeen']

            return ObservedTime(start_time=start_date,
                                end_time=end_date)

        def _timestamp(self, finding):
            unix_timestamp = self.root.service(finding)['EventLastSeen']
            return self.root.time_format(
                datetime.utcfromtimestamp(unix_timestamp)
            )

        def _source_uri(self, finding):
            return SOURCE_URI.format(
                region=self.root.aws_region, finding_id=finding['Id']
            )

        def _relations(self, finding):
            def relation(source, type_, target):
                source_type, source_value = source
                target_type, target_value = target

                if not source or not target:
                    return None

                return ObservedRelation(
                    origin=SOURCE,
                    related=Observable(type=target_type,
                                       value=target_value),
                    relation=type_,
                    source=Observable(type=source_type,
                                      value=source_value)
                )

            action_type = self.root.action_type(finding)
            data = self.root.action_data(finding, action_type)
            if action_type == NETWORK_CONNECTION:
                source, target = DIRECTION[data['ConnectionDirection']]
                yield relation(
                    ['ip', self.root.ip(data, source)],
                    'Connected_To',
                    ['ip', self.root.ip(data, target)]
                )

        def _targets(self, finding):
            return IdentitySpecification(
                observables=[
                    x for x in self.observables(finding) if x is not None
                ],
                observed_time=self._observed_time(finding),
                type=SENSOR
            )

        def extract(self, finding):

            return Sighting(
                observables=[self.root.observable],
                title=finding['Title'],
                description=finding['Description'],
                observed_time=self._observed_time(finding),
                source_uri=self._source_uri(finding),
                timestamp=finding['UpdatedAt'],
                count=finding['Service']['Count'],
                severity=SEVERITY[int(finding['Severity'])],
                relations=[x for x in self._relations(finding) if x],
                targets=[self._targets(finding)],
                **SIGHTING_DEFAULTS
            ).json
