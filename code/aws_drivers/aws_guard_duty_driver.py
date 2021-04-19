import boto3

from flask import current_app
from api.errors import GuardDutyError
from botocore.exceptions import (
    BotoCoreError,
    ClientError
)


def handle_exceptions(f):
    memo = {}

    def wraps(*args):
        if args[0] not in memo:
            try:
                memo[args[0]] = f(*args)
            except (BotoCoreError, ValueError, ClientError) as error:
                raise GuardDutyError(error.args[0])
        return memo[args[0]]

    return wraps


class GuardDutyDriver(object):
    """
    Class for working with AWS GuardDuty resource
    """

    def __init__(self):
        self.region = str(current_app.config['AWS_REGION'])
        self.access_key = str(current_app.config['AWS_ACCESS_KEY_ID'])
        self.secret_access_key = str(current_app.config['AWS_SECRET_ACCESS_KEY'])
        self.driver = boto3.client(
            'guardduty', self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_access_key
        )
        self.findings = self.Finding(self)

    class Finding:

        def __init__(self, root):
            self.driver = root.driver
            self.max_results = 50
            self.findings = []
            self.ctr_limit = current_app.config['CTR_ENTITIES_LIMIT']
            self.detector = current_app.config['AWS_GUARD_DUTY_DETECTOR_ID']

        @handle_exceptions
        def get(self, criterion, limit=None, next_token=''):
            limit = self.ctr_limit if not limit else limit

            response = self.driver.list_findings(
                DetectorId=self.detector,
                FindingCriteria=criterion,
                MaxResults=limit if limit <= self.max_results
                else self.max_results,
                NextToken=next_token
            )

            findings = self.driver.get_findings(
                DetectorId=self.detector,
                FindingIds=response.get('FindingIds')
            ).get('Findings')

            for finding in findings:
                if len(self.findings) < self.ctr_limit:
                    self.findings.append(finding)

            next_token = response.get('NextToken')
            if next_token and len(self.findings) < self.ctr_limit:
                self.get(criterion, limit - self.max_results, next_token)

            return self.findings
