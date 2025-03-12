class NotFoundException(Exception):
    """Raised when the specified file is not found."""

    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)


class AuthenticationError(Exception):
    """Raised when user authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        self.message = message
        super().__init__(self.message)


class AccessDeniedException(Exception):
    """Raised when user has no access to the project/document"""

    def __init__(self, message: str = "Access denied"):
        self.message = message
        super().__init__(self.message)


class InvalidDataFormatError(Exception):
    """Raised when data doesn't match the expected format."""

    def __init__(self, message: str = "Invalid data format"):
        self.message = message
        super().__init__(self.message)


class PostFailedException(Exception):
    def __init__(self, message="Failed to create data"):
        self.message = message
        super().__init__(message)


class UpdateFailedException(Exception):
    def __init__(self, message="Failed to update data"):
        self.message = message
        super().__init__(message)


class DeleteFailedException(Exception):
    def __init__(self, message="Failed to delete data"):
        self.message = message
        super().__init__(message)


class InvalidInputException(Exception):
    def __init__(self, message="Invalid data input"):
        self.message = message
        super().__init__(message)
