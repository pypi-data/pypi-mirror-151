from starlette.exceptions import HTTPException as HTTPException

class AppConfigurationError(Exception):
    pass

class InvalidTypeError(Exception):
    pass

class UnknownError(Exception):
    pass
