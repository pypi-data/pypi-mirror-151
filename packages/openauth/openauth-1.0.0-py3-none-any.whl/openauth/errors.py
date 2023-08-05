class ValidationFailedException(Exception):
    pass


class UserExistsException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class InvalidPasswordException(Exception):
    pass


class LinkExpiredException(Exception):
    pass


class IncorrectEmailException(Exception):
    pass
