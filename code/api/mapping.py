from flask import current_app
from api.utils import RangeDict
from bundlebuilder.session import Session
from bundlebuilder.models import (
    Observable,
    ObservedTime,
    ObservedRelation,
    IdentitySpecification,
    Sighting,
    Indicator,
    ValidTime,
    Relationship,
    SightingDataTable,
    ColumnDefinition
)
from types import SimpleNamespace

CONFIDENCE = "High"
SIGHTING = "sighting"
SENSOR = "network.ips"
PORT_PROBE = "PORT_PROBE"
DNS_REQUEST = "DNS_REQUEST"
ID_PREFIX = "aws-guard-duty"
AWS_API_CALL = "AWS_API_CALL"
SOURCE = "Amazon GuardDuty findings"
NETWORK_CONNECTION = "NETWORK_CONNECTION"
DEFAULT_VALID_END_DATE = "2525-01-01T00:00:00.000Z"

SOURCE_URI = (
    "https://console.aws.amazon.com/guardduty/home?"
    "{region}/findings&region={region}#/findings?"
    "macros=all&fId={finding_id}&search=id%3D{finding_id}"
)

SEVERITY = RangeDict({
    range(7, 9): "High",
    range(4, 7): "Medium",
    range(1, 4): "Low"
})

DEFAULTS = {
    "confidence": CONFIDENCE,
    "source": SOURCE
}

COLUMNS_MAPPING = (
    ("sensor name", "ServiceName"),
    ("asn", "Asn"),
    ("asn org", "AsnOrg"),
    ("org", "Org"),
    ("isp", "Isp"),
    ("country", "CountryName"),
    ("city", "CityName"),
    ("local port", "Port"),
    ("local port name", "PortName")
)


class Mapping:

    def __init__(self, data, **observable):
        self.finding = data
        self.observable = Observable(**observable)
        self.aws_region = current_app.config["AWS_REGION"]
        self._session = Session(
            external_id_prefix=ID_PREFIX,
            source=SOURCE,
            source_uri=self._source_uri(),
        )

    def set_session(self):
        return self._session.set()

    def _severity(self):
        return SEVERITY[int(self.finding.Severity)]

    def _source_uri(self):
        return SOURCE_URI.format(
            region=self.aws_region, finding_id=self.finding.Id
        )

    def _observed_time(self):
        start_date = self.finding.Service.EventFirstSeen
        end_date = self.finding.Service.EventLastSeen

        return ObservedTime(start_time=start_date,
                            end_time=end_date)

    def _observables(self):
        interfaces = \
            self.finding.Resource.InstanceDetails.NetworkInterfaces
        for data in interfaces:
            yield Observable(type="ip", value=data.PublicIp)
            yield Observable(type="ip", value=data.PrivateIpAddress)
            for ipv6_address in data.Ipv6Addresses:
                yield Observable(type="ipv6", value=ipv6_address)
            yield Observable(type="domain", value=data.PublicDnsName)

    @staticmethod
    def _relation(source, type_, target):
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

    def _relations(self):
        action_type = self.finding.Service.Action.ActionType
        if action_type == NETWORK_CONNECTION:
            action = self.finding.Service.Action.NetworkConnectionAction
            local_ip = action.LocalIpDetails.IpAddressV4
            remote_ip = action.RemoteIpDetails.IpAddressV4
            directions = {
                "INBOUND": [remote_ip, local_ip],
                "OUTBOUND": [local_ip, remote_ip]
            }
            direction = action.ConnectionDirection
            source, target = directions[direction]
            yield self._relation(
                ["ip", source], "Connected_To", ["ip", target]
            )

    def _targets(self):
        return IdentitySpecification(
            observables=[
                x for x in self._observables() if x is not None
            ],
            observed_time=self._observed_time(),
            type=SENSOR
        )

    def _data(self):
        action = self.finding.Service.Action
        action_key = action.ActionType.replace("_", " ")
        action_key = action_key.title().replace(" ", "") + "Action"
        action_data = getattr(
            action,
            action_key
        )
        remote_data = action_data.RemoteIpDetails.Organization
        local_data = action_data.LocalPortDetails
        return SimpleNamespace(
            **remote_data.__dict__,
            **local_data.__dict__,
            **{"ServiceName": self.finding.Service.ServiceName}
        )

    def _data_table(self):
        attrs = self._data()
        columns = []
        rows = []

        for key, value in COLUMNS_MAPPING:
            if value in [attr for attr in dir(attrs) if "__" not in attr]:
                columns.append(ColumnDefinition(name=key, type="string"))
                rows.append(getattr(attrs, value))

        return SightingDataTable(
            columns=columns,
            rows=[rows],
            row_count=1
        ).json

    def extract_sighting(self):

        sighting = Sighting(
            internal=True,
            observables=[self.observable],
            title=self.finding.Title,
            description=self.finding.Description,
            observed_time=self._observed_time(),
            source_uri=self._source_uri(),
            timestamp=self.finding.Service.EventLastSeen,
            count=self.finding.Service.Count,
            severity=self._severity(),
            relations=[x for x in self._relations() if x],
            targets=[self._targets()],
            sensor=SENSOR,
            **DEFAULTS
        )

        if self.finding.Service.Action.ActionType in [
            NETWORK_CONNECTION,
            PORT_PROBE
        ]:
            sighting.json["data"] = self._data_table()
        return sighting

    def extract_indicator(self):
        start_time = self.finding.Service.EventFirstSeen
        description = self.finding.Description

        return Indicator(
            producer=SENSOR,
            valid_time=ValidTime(
                start_time=start_time,
                end_time=DEFAULT_VALID_END_DATE
            ),
            description=description,
            short_description=description,
            severity=self._severity(),
            source_uri=self._source_uri(),
            timestamp=start_time,
            **DEFAULTS
        )

    @staticmethod
    def extract_relationship(source_ref, target_ref, type_):
        return Relationship(
            source_ref=source_ref,
            target_ref=target_ref,
            relationship_type=type_
        )
