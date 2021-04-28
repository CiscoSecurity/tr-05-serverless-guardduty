from bundlebuilder.models import (
    Observable,
    ObservedTime,
    ObservedRelation,
    IdentitySpecification
)
from bundlebuilder.models import Sighting as SightingModel


class Sighting:

    LOCAL_IP = 'LocalIpDetails'
    REMOTE_IP = 'RemoteIpDetails'

    DIRECTION = {
        'INBOUND': (REMOTE_IP, LOCAL_IP),
        'OUTBOUND': (LOCAL_IP, REMOTE_IP)
    }

    def __init__(self, root):
        self.root = root
        self.finding = root.data

    def _observed_time(self):
        service = self.root.service()
        start_date = service['EventFirstSeen']
        end_date = service['EventLastSeen']

        return ObservedTime(start_time=start_date,
                            end_time=end_date)

    def _observable(self, type_, value):
        interfaces = \
            self.finding['Resource']['InstanceDetails']['NetworkInterfaces']

        for data in interfaces:
            if data.get(value):
                return Observable(type=type_, value=data[value])

    def _observables(self):

        yield self._observable('ip', 'PublicIp')
        yield self._observable('domain', 'PublicDnsName')

    def _relation(self, source, type_, target):
        source_type, source_value = source
        target_type, target_value = target

        if not source or not target:
            return None

        return ObservedRelation(
            origin=self.root.SOURCE,
            related=Observable(type=target_type,
                               value=target_value),
            relation=type_,
            source=Observable(type=source_type,
                              value=source_value)
        )

    def _relations(self):

        action_type = self.root.action_type()
        data = self.root.action_data(action_type)
        if action_type == self.root.NETWORK_CONNECTION:
            source, target = self.DIRECTION[data['ConnectionDirection']]
            yield self._relation(
                ['ip', data[source]['IpAddressV4']],
                'Connected_To',
                ['ip', data[target]['IpAddressV4']]
            )

    def _targets(self):
        return IdentitySpecification(
            observables=[
                x for x in self._observables() if x is not None
            ],
            observed_time=self._observed_time(),
            type=self.root.SENSOR
        )

    def extract(self):
        service = self.root.service()
        return SightingModel(
            observables=[self.root.observable],
            title=self.finding['Title'],
            description=self.finding['Description'],
            observed_time=self._observed_time(),
            source_uri=self.root.source_uri(),
            timestamp=service['EventLastSeen'],
            count=self.finding['Service']['Count'],
            severity=self.root.severity(),
            relations=[x for x in self._relations() if x],
            targets=[self._targets()],
            sensor=self.root.SENSOR,
            **self.root.DEFAULTS
        ).json
