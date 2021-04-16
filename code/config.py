import json


class Config:
    settings = json.load(open('container_settings.json', 'r'))
    VERSION = settings['VERSION']

    DEFAULT_AWS_REGION = 'us-east-1'
    DEFAULT_CTR_ENTITIES_LIMIT = 100
