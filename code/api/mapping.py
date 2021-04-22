from datetime import datetime
from flask import current_app
from api.utils import RangeDict

from bundlebuilder.models import (
    ObservedRelation,
    Observable,
    Sighting,
    ObservedTime
)

CTIM_DEFAULTS = {
    'schema_version': '1.1.5'
}
SOURCE = 'AWS Guard Duty'
SIGHTING = 'sighting'

SIGHTING_DEFAULTS = {
    'confidence': 'High',
    'source': SOURCE
}

SOURCE_URI = \
    'https://console.aws.amazon.com/guardduty/home?' \
    '{region}/findings?macros=current&fId={finding_id}'

INBOUND = 'INBOUND'
OUTBOUND = 'OUTBOUND'

CONNECTION = {
    INBOUND: 'Connected_From',
    OUTBOUND: 'Connected_To'
}

NETWORK_CONNECTION = 'NETWORK_CONNECTION'
PORT_PROBE = 'PORT_PROBE'
DNS_REQUEST = 'DNS_REQUEST'
AWS_API_CALL = 'AWS_API_CALL'

SEVERITY = RangeDict({
    range(7, 9): 'High',
    range(4, 7): 'Medium',
    range(1, 4): 'Low'
})


class Mapping:

    def __init__(self, type_, value):
        self.observable = Observable(
            type=type_,
            value=value
        )
        self.aws_region = current_app.config['AWS_REGION']
        self.sighting = self.Sighting(self)

    @staticmethod
    def date(date_):
        date_str = datetime.strptime(date_, '%Y-%m-%dT%H:%M:%S.%fZ')
        date_ = f'{date_str.isoformat(timespec="seconds")}Z'
        return date_

    @staticmethod
    def ip(action, type_):
        return action[type_]['IpAddressV4']

    @staticmethod
    def action(data):
        return data['Service']['Action']

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

    def direction(self, finding):
        action = self.action_data(finding, NETWORK_CONNECTION)
        return CONNECTION[action['ConnectionDirection']]

    class Sighting:
        def __init__(self, root):
            self.root = root

        def _observed_time(self, finding):
            start_date = self.root.date(finding['CreatedAt'])
            end_date = self.root.date(finding['UpdatedAt'])

            return ObservedTime(start_time=start_date,
                                end_time=end_date)

        def _timestamp(self, finding):
            unix_timestamp = finding['UpdatedAt']
            return self.root.time_format(
                datetime.utcfromtimestamp(unix_timestamp)
            )

        def _source_uri(self, finding):
            return SOURCE_URI.format(
                region=self.root.aws_region, finding_id=finding['Id']
            )

        def _relations(self, finding):
            def relation(source, target, type_):
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
                yield relation(
                    ['ip', self.root.ip(data, 'LocalIpDetails')],
                    ['ip', self.root.ip(data, 'RemoteIpDetails')],
                    self.root.direction(finding)
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
                **SIGHTING_DEFAULTS
            ).json
