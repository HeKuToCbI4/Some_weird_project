class Failure(BaseException):
    def __init__(self, message, errors=None):
        super(Failure, self).__init__(message)
        self.errors = errors if errors else None
