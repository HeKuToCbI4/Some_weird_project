class Failure(BaseException):
    def __init__(self, message, errors):
        super(Failure, self).__init__(message)
        self.errors = errors

