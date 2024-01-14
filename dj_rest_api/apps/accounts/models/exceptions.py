class UserNotCreatedException(Exception):
    """Raised when there is an error creating a user."""

    def __init__(self, detail):
        super().__init__(f"User creation error: {detail}")
        self.detail = detail

    def __str__(self):
        return self.args[0]


class UserNotFoundException(Exception):
    """Raised when user not existed."""

    def __init__(self, detail):
        super().__init__("User user is not found")
        self.detail = detail

    def __str__(self):
        return self.args[0]
