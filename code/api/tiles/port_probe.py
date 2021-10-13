from api.tiles.factory import ITile


class PortProbeTile(ITile):
    @property
    def _id(self):
        return "port_probe_source_countries"

    @property
    def _type(self):
        return "threat_map"

    @property
    def _tags(self):
        return [self._id]

    @property
    def _title(self):
        return "Port Probe Source Countries"

    @property
    def _description(self):
        return (
            f"{self._title} tile visualizes "
            "the countries where port probes "
            "are issued from."
        )

    @property
    def _short_description(self):
        return self._description

    @property
    def _periods(self):
        return {
            "last_24_hours": 1,
            "last_7_days": 7,
            "last_30_days": 30,
            "last_60_days": 60,
            "last_90_days": 90
        }

    def finding_criteria(self, period):
        criterion = \
            super(PortProbeTile, self).finding_criteria(period)
        criterion["Criterion"].update(
            {
                "service.action.actionType": {
                    "Equals": [
                        "PORT_PROBE"
                    ]
                }
            }
        )
        return criterion

    @staticmethod
    def _locations(finding):
        return finding.Service.Action.PortProbeAction.PortProbeDetails

    def data(self, findings):
        data = []
        for finding in findings:
            locations = self._locations(finding)
            for location in locations:
                details = location.RemoteIpDetails
                point = dict(
                    coordinates=list(details.GeoLocation.__dict__.values()),
                    ip_address=details.IpAddressV4,
                    volume=finding.Service.Count,
                    email_type="N/A",
                    hostname="N/A"
                )
                if point not in data:
                    data.append(point)

        return data

    def tile_data(self, findings, period):
        return {
            "data": self.data(findings),
            **self.tile_extra_data(period)
        }
