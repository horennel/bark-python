class BarkError(Exception):
    """
    所有 Bark 异常的基类。
    Base exception class for Bark operations.
    """
    pass


class APIRequestError(BarkError):
    """
    请求服务器失败时抛出。
    Raised when an API request fails.
    """
    pass


class InvalidParameterError(BarkError):
    """
    参数不合法时抛出。
    Raised when input parameters are invalid.
    """
    pass
