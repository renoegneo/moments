class RegistrationError(Exception):
    def __init__(self, message: str, code: int = 409):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AuthenticationError(Exception):
    def __init__(self, message: str = "Неверный логин или пароль", code: int = 401):
        self.message = message
        self.code = code
        super().__init__(self.message)