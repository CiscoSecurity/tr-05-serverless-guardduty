import boto3

from flask import current_app


class GuardDutyDriver(object):
    """
    Class for working with AWS GuardDuty resource
    """

    def __init__(self):
        self.region = current_app.config['AWS_REGION']
        self.access_key = current_app.config['AWS_ACCESS_KEY_ID']
        self.secret_access_key = current_app.config['AWS_SECRET_ACCESS_KEY']
        self.driver = boto3.client(
            'guardduty', self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_access_key
        )
        self.findings = self.Finding(self)

    class Finding:
        def __init__(self, root):
            self.driver = root.driver

        def list(self, detector_id, criterion, max_results=20, next_token=''):
            response = self.driver.list_findings(
                DetectorId=detector_id,
                FindingCriteria=criterion,
                MaxResults=max_results,
                NextToken=next_token
            )
            finding_ids = response.get('FindingIds')
            return finding_ids
