class ValidationError(Exception):
    def __init__(self, message="Validation failed", errors=None):
        super().__init__(message)
        self.message = message
        self.errors = errors or []