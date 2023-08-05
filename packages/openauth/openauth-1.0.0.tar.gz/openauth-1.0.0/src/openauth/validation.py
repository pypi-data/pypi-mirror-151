import re

EMAIL = re.compile(r"^\w+([-+.\']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
USERNAME = re.compile(r"^[a-zA-Z0-9_\-\.]{4,}$")
PASSWORD = re.compile(
    r"(?=(.*[0-9]))(?=.*[\\!@#$%^&*()\[\]{}\-_+=~`|:;\"\'<>,.\/?])(?=.*[a-z])(?=(.*[A-Z]))(?=(.*)).{8,}"
)


def validate_username(username: str) -> bool:
    if USERNAME.match(username) is not None:
        return True
    return False


def validate_email(email: str) -> bool:
    if EMAIL.match(email) is not None:
        return True
    return False


def validate_password(password: str) -> bool:
    if PASSWORD.match(password) is not None:
        return True
    return False
