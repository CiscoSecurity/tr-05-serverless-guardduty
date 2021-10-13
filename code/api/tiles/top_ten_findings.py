from api.tiles.factory import ITile


class TopTenFindingsTile(ITile):
    @property
    def _id(self):
        return "top_ten_findings"

    @property
    def _type(self):
        return "markdown"

    @property
    def _tags(self):
        return [self._id]

    @property
    def _title(self):
        return "Top 10 Findings by count"

    @property
    def _description(self):
        return (
            f"{self._title} tile provides a list "
            f"of the top 10 findings by count."
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

    @property
    def limit(self):
        return 10

    @property
    def sort_criteria(self):
        return {
            "AttributeName": "service.count",
            "OrderBy": "DESC"
        }

    def tile_data(self, findings, period):
        row = "| {number} | {description} | {count} |"
        table = [
            "|  №  | Description | Count |",
            "| --- | ----------- | ----- |"
        ]
        table.extend(
            [row.format(
                number=index+1,
                description=item.Description,
                count=item.Service.Count
            ) for index, item in enumerate(findings)]
        )
        return {
            "data": table,
            **self.tile_extra_data(period)
        }
