"""Exception."""


class CodeException(Exception):
    """Get code thread exception."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class TimeoutException(Exception):
    """Get code timeout exception."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class StoreNotFound(Exception):
    """Store not found exception."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class InvalidStore(Exception):
    """Invalide store exception."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo


class SameStore(Exception):
    """Raise when switch to the same store."""

    def __init__(self, exc_info):
        """Initialize the exception."""
        super().__init__(self)
        self.errorinfo = exc_info

    def __str__(self):
        """str."""
        return self.errorinfo
