class APILimitReached(Exception):
    """Raised when API Limit is reached"""

class EntityTooLarge(Exception):
    """Raised when image size > 10MB"""

class ServerError(Exception):
    """Something wrong with the trace.moe server or Image provided was malformed"""
 
class IvalidToken(Exception):
    """Ivalid token was provided"""
    
class EmptyImage(Exception):
    """Image provided was empty"""
