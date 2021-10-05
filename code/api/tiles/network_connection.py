from api.tiles.port_probe import PortProbeTile


class NetworkConnectionTile(PortProbeTile):

    @property
    def _id(self):
        return "network_connection_source_countries"

    @property
    def _type(self):
        return "threat_map"

    @property
    def _tags(self):
        return [self._id]

    @property
    def _title(self):
        return "Network Connection Source Countries"

    @property
    def _description(self):
        return (
            f"{self._title} tile visualizes "
            f"the countries where port probes "
            f"are issued from."
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
            super(NetworkConnectionTile, self).finding_criteria(period)
        criterion["Criterion"].update(
            {
                "service.action.actionType": {
                    "Equals": [
                        "NETWORK_CONNECTION"
                    ]
                }
            }
        )
        return criterion

    @staticmethod
    def _locations(finding):
        return [finding.Service.Action.NetworkConnectionAction]
