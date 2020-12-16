"""Exception classes for all of pyentrez."""


class PyEntrezException(Exception):
    """Plain Flake8 exception."""


class EarlyQuit(PyEntrezException):
    """Except raised when encountering a KeyboardInterrupt."""


class ExecutionError(PyEntrezException):
    """Exception raised during execution of pyentrez."""
