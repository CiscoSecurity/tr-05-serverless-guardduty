import json


class Config:
    settings = json.load(open('container_settings.json', 'r'))
    VERSION = settings['VERSION']

    DEFAULT_CTR_ENTITIES_LIMIT = 100

    GUARD_DUTY_REFER_URL = \
        'https://{region}.console.aws.amazon.com/detective/' \
        'home?region={region}#entities/IpAddress/' \
        '{observable}?scopeStart=1618333200000&scopeEnd=1618390800000&r=760'
