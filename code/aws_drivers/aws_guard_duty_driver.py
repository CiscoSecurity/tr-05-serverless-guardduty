import boto3

from flask import current_app
from api.errors import (
    GDRegionError,
    GDAuthError,
    GDParamsValidationError,
    GDBadRequestError
)
from botocore.exceptions import (
    NoRegionError,
    NoCredentialsError,
    PartialCredentialsError,
    ParamValidationError,
    EndpointConnectionError
)

expected_errors = {
    NoRegionError: GDRegionError,
    PartialCredentialsError: GDAuthError,
    NoCredentialsError: GDAuthError,
    ParamValidationError: GDParamsValidationError,
    EndpointConnectionError: GDRegionError,
    ValueError: GDBadRequestError
}


class GuardDutyDriver(object):
    """
    Class for working with AWS GuardDuty resource
    """

    def __init__(self):
        self.region = current_app.config['AWS_REGION']
        self.access_key = current_app.config['AWS_ACCESS_KEY_ID']
        self.secret_access_key = current_app.config['AWS_SECRET_ACCESS_KEY']
        try:
            self.driver = boto3.client(
                'guardduty', self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_access_key
            )
        except tuple(expected_errors) as error:
            raise expected_errors[error.__class__](error.args[0])

        self.findings = self.Finding(self)

    class Finding:

        def __init__(self, root):
            self.driver = root.driver
            self.detector = current_app.config['AWS_GUARD_DUTY_DETECTOR_ID']

        def list(self, criterion, max_results=20, next_token=''):
            try:
                response = self.driver.list_findings(
                    DetectorId=self.detector,
                    FindingCriteria=criterion,
                    MaxResults=max_results,
                    NextToken=next_token
                )
                return response.get('FindingIds')
            except tuple(expected_errors) as error:
                raise expected_errors[error.__class__](error.args[0])
            except (self.driver.exceptions.InternalServerErrorException,
                    self.driver.exceptions.BadRequestException) as error:
                raise GDBadRequestError(error.args[0])
