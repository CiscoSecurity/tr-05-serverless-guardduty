UNKNOWN = 'unknown'
AUTH_ERROR = 'authorization error'
INVALID_ARGUMENT = 'invalid argument'
HEALTH_CHECK_ERROR = 'health check failed'
AWS_REGION_ERROR = 'aws region error'
AWS_PARAMS_ERROR = 'aws params error'
AWS_REQUEST_ERROR = 'aws request error'
AWS_CREDENTIALS_ERROR = 'aws credentials error'


class TRFormattedError(Exception):
    def __init__(self, code, message, type_='fatal'):
        super().__init__()
        self.code = code or UNKNOWN
        self.message = message or 'Something went wrong.'
        self.type_ = type_

    @property
    def json(self):
        return {'type': self.type_,
                'code': self.code,
                'message': self.message}


class AuthorizationError(TRFormattedError):
    def __init__(self, message):
        super().__init__(
            AUTH_ERROR,
            f'Authorization failed: {message}'
        )


class InvalidArgumentError(TRFormattedError):
    def __init__(self, message):
        super().__init__(
            INVALID_ARGUMENT,
            str(message)
        )


class WatchdogError(TRFormattedError):
    def __init__(self):
        super().__init__(
            code=HEALTH_CHECK_ERROR,
            message='Invalid Health Check'
        )


class GDRegionError(TRFormattedError):
    def __init__(self, message):
        super().__init__(
            code=AWS_REGION_ERROR,
            message=message
        )


class GDAuthError(TRFormattedError):
    def __init__(self, message):
        super().__init__(
            code=AWS_CREDENTIALS_ERROR,
            message=f'Authorization failed: {message}'
        )


class GDParamsValidationError(TRFormattedError):
    def __init__(self, message):
        super().__init__(
            code=AWS_PARAMS_ERROR,
            message=message
        )


class GDBadRequestError(TRFormattedError):
    def __init__(self, message):
        super().__init__(
            code=AWS_REQUEST_ERROR,
            message=message
        )
