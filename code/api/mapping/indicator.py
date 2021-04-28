from bundlebuilder.models import Indicator as IndicatorModel, ValidTime


class Indicator:
    def __init__(self, root):
        self.root = root
        self.finding = root.data

    def extract(self):
        service = self.root.service()
        start_time = service['EventFirstSeen']
        return IndicatorModel(
            producer=self.root.SENSOR,
            valid_time=ValidTime(start_time=start_time),
            description=self.finding['Description'],
            short_description=self.finding['Description'],
            severity=self.root.severity(),
            source_uri=self.root.source_uri(),
            timestamp=start_time,
            **self.root.DEFAULTS
        ).json
