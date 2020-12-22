"""All erorrs that are raised."""


class APIError(Exception):

    "Base for all errors"


class TooManyRequests(APIError):

    "Raised when API Limit is reached or Too many requests in short period of time"


class EntityTooLarge(APIError):

    """Raised when image size > 10MB"""


class ServerError(APIError):

    "Something wrong with the trace.moe server or Image provided was malformed"


class InvalidToken(APIError):

    "Invalid token was provided"

class EmptyImage(APIError):

    "Image provided was empty"

class InvalidPath(Exception):

    "Given path doesn't exist."
