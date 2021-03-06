from api.tiles.factory import ITile


class AffectedInstancesTile(ITile):

    @property
    def _id(self):
        return "affected_instances"

    @property
    def _type(self):
        return "donut_graph"

    @property
    def _tags(self):
        return [self._id]

    @property
    def _title(self):
        return "Affected Instances"

    @property
    def _description(self):
        return (
            f"{self._title} tile shows "
            "what types of findings EC2 instances have."
        )

    @property
    def _short_description(self):
        return (
            f"{self._title} by finding types "
            "for given time period."
        )

    @property
    def _periods(self):
        return {
            "last_24_hours": 1,
            "last_7_days": 7,
            "last_30_days": 30
        }

    @staticmethod
    def affected_iscs_id(findings):
        return list(
            set(
                [
                    finding.Resource.InstanceDetails.InstanceId for finding
                    in findings
                ]
            )
        )

    @staticmethod
    def finding_types(findings):
        return list(
            sorted(
                set(
                    [finding.Type for finding in findings]
                )
            )
        )

    @staticmethod
    def _sum_of_findings_by_isc(instance, findings):
        return sum(
            finding.Resource.InstanceDetails.InstanceId == instance for finding
            in findings
        )

    def _segments(self, instance, findings):
        def segment(_type):
            return {
                "key": self.finding_types(findings).index(_type),
                "value": sum(
                    finding.Type == _type and
                    finding.Resource.InstanceDetails.InstanceId == instance
                    for finding in findings
                )
            }

        return [segment(_type) for _type in self.finding_types(findings)]

    def _data(self, instance, findings):
        return {
            "key": self.affected_iscs_id(findings).index(instance),
            "value": self._sum_of_findings_by_isc(instance, findings),
            "segments": self._segments(instance, findings)
        }

    def finding_criteria(self, period):
        criterion = super(AffectedInstancesTile, self).finding_criteria(period)
        criterion["Criterion"].update(
            {
                "resource.resourceType": {
                    "Equals": [
                        "Instance"
                    ]
                }
            }
        )
        return criterion

    def tile_data(self, findings, period):
        return {
                "label_headers": [
                    "Affected instances",
                    "Finding types"
                ],
                "labels": [
                    self.affected_iscs_id(findings),
                    self.finding_types(findings)
                ],
                "data": [
                    self._data(instance, findings) for instance
                    in self.affected_iscs_id(findings)
                ],
                **self.tile_extra_data(period)
            }
