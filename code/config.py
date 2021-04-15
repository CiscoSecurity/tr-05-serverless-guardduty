import json


class Config:
    settings = json.load(open('container_settings.json', 'r'))
    VERSION = settings['VERSION']

    DEFAULT_AWS_ACCESS_KEY_ID = None
    DEFAULT_AWS_SECRET_ACCESS_KEY = None
    DEFAULT_AWS_GUARD_DUTY_DETECTOR_ID = None
    DEFAULT_AWS_REGION = 'us-east-1'

    HEALTH_CHECK_OBSERVABLE = {"type": "ip", "value": "1.1.1.1"}

