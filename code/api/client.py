import json
import boto3
import botocore
from types import SimpleNamespace

from flask import current_app
from botocore.exceptions import (
    BotoCoreError,
    ClientError
)
from api.errors import GuardDutyError


def serialize(obj):
    return json.loads(
        json.dumps(obj, default=str),
        object_hook=lambda d: SimpleNamespace(**d)
    )


class GuardDuty(object):
    """
    Class for working with Amazon GuardDuty resource
    """

    DEFAULT_ORDER = {
        'AttributeName': 'service.eventLastSeen',
        'OrderBy': 'DESC'
    }

    def __init__(self):

        self._token = ''
        self._findings = []
        self.max_results = 50
        self.driver = self._connect()

        self.detector = str(
            current_app.config['AWS_GUARD_DUTY_DETECTOR_ID']
        )
        self.ctr_limit = self._set_ctr_limit(
            current_app.config['CTR_ENTITIES_LIMIT']
        )

    @staticmethod
    def _connect():
        secret_key = str(
            current_app.config['AWS_SECRET_ACCESS_KEY']
        )
        config = botocore.config.Config(
            user_agent=current_app.config['USER_AGENT']
        )
        access_key = str(
            current_app.config['AWS_ACCESS_KEY_ID']
        )
        region = str(
            current_app.config['AWS_REGION']
        )

        try:
            return boto3.client(
                'guardduty',
                aws_secret_access_key=secret_key,
                aws_access_key_id=access_key,
                region_name=region,
                config=config
            )
        except ValueError as error:
            raise GuardDutyError(error.args[0])

    @property
    def findings(self):
        return self._findings

    @findings.setter
    def findings(self, values):
        for value in values:
            if len(self.findings) < self.ctr_limit:
                if value not in self.findings:
                    self.findings.append(serialize(value))

    @staticmethod
    def _set_ctr_limit(limit):
        try:
            ctr_limit = int(limit)
            assert ctr_limit > 0
        except (ValueError, AssertionError):
            ctr_limit = \
                current_app.config['DEFAULT_CTR_ENTITIES_LIMIT']
        return ctr_limit

    def _look_up_for_data(self, **kwargs):
        try:
            data = self.driver.list_findings(
                DetectorId=self.detector,
                NextToken=self._token,
                **kwargs
            )

            findings = self.driver.get_findings(
                DetectorId=self.detector,
                FindingIds=data.get('FindingIds')
            ).get('Findings')

        except (BotoCoreError, ValueError, ClientError) as error:
            if hasattr(error, 'operation_name'):
                if error.operation_name == 'ListFindings' and \
                        error.response.get('Type') == 'InternalException':
                    return []
            raise GuardDutyError(error.args[0])

        self._token = data.get('NextToken')

        return findings

    def search(self, criteria, order=None, limit=None,
               unlimited=False):

        limit = self.ctr_limit if not limit else limit

        self.findings = self._look_up_for_data(
            FindingCriteria=criteria,
            SortCriteria=order or self.DEFAULT_ORDER,
            MaxResults=limit if limit <= self.max_results
            else self.max_results
        )
        if self._token:
            if 0 < len(self._findings) < self.ctr_limit or unlimited:
                limit = limit - self.max_results
                self.search(criteria=criteria, limit=limit)

    def health(self):
        try:
            response = self.driver.get_detector(
                DetectorId=self.detector
            )
        except (BotoCoreError, ValueError, ClientError) as error:
            raise GuardDutyError(error.args[0])
        return response
