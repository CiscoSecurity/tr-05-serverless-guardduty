import re

from .finding import Finding
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

CONFIDENCE = "High"
SIGHTING = "sighting"
SENSOR = "network.ips"
PORT_PROBE = "PORT_PROBE"
DNS_REQUEST = "DNS_REQUEST"
ID_PREFIX = "aws-guard-duty"
AWS_API_CALL = "AWS_API_CALL"
SOURCE = "AWS GuardDuty findings"
NETWORK_CONNECTION = "NETWORK_CONNECTION"
DEFAULT_VALID_END_DATE = "2525-01-01T00:00:00.000Z"

SOURCE_URI = (
    "https://console.aws.amazon.com/guardduty/home?"
    "{region}/findings&region={region}#/findings?"
    "macros=current&fId={finding_id}"
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
        self.finding = Finding(data)
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
        return SEVERITY[int(self.finding.severity)]

    def _source_uri(self):
        return SOURCE_URI.format(
            region=self.aws_region, finding_id=self.finding.id
        )

    def _observed_time(self):
        start_date = self.finding.service.first_seen
        end_date = self.finding.service.last_seen

        return ObservedTime(start_time=start_date,
                            end_time=end_date)

    def _observables(self):
        interfaces = \
            self.finding.resource.details.interfaces
        for data in interfaces:
            yield Observable(type="ip", value=data.PublicIp)
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
        action_type = self.finding.service.action.type
        if action_type == NETWORK_CONNECTION:
            source, target = self.finding.service.action.data.direction()
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

    def _data_table(self):
        attrs = self.finding.service.attrs()
        columns = []
        rows = []

        for key, value in COLUMNS_MAPPING:
            if value in attrs.keys():
                columns.append(ColumnDefinition(name=key, type="string"))
                rows.append([attrs[value]])

        return SightingDataTable(
            columns=columns,
            rows=rows
        ).json

    def extract_sighting(self):

        sighting = Sighting(
            observables=[self.observable],
            title=self.finding.title,
            description=self.finding.description,
            observed_time=self._observed_time(),
            source_uri=self._source_uri(),
            timestamp=self.finding.service.last_seen,
            count=self.finding.service.count,
            severity=self._severity(),
            relations=[x for x in self._relations() if x],
            targets=[self._targets()],
            sensor=SENSOR,
            **DEFAULTS
        )

        if self.finding.service.action.type in [
            NETWORK_CONNECTION,
            PORT_PROBE
        ]:
            sighting.json["data"] = self._data_table()
        return sighting

    def extract_indicator(self):
        start_time = self.finding.service.first_seen
        description = self.finding.description

        # Delete AWS instance id and
        # unnecessary space in indicator description.
        formatted_description = \
            re.sub(r"(i)-[0-9a-z]+", "", description).replace("  ", " ")

        return Indicator(
            producer=SENSOR,
            valid_time=ValidTime(
                start_time=start_time,
                end_time=DEFAULT_VALID_END_DATE
            ),
            description=formatted_description,
            short_description=formatted_description,
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
