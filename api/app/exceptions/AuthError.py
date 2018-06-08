# Format error response and append state code.
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code