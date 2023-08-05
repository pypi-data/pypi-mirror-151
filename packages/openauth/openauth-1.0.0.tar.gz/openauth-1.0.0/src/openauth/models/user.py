import bcrypt
from deta import Deta

from ..errors import ValidationFailedException, UserExistsException
from ..validation import validate_username, validate_email, validate_password


class User:
    def __init__(self, db: Deta.Base, email: str, username: str, password: str):
        self.email = email
        self.username = username
        self.password = password
        self.db = db

    def update_username(self, new_username: str) -> None:
        if validate_username(new_username) is False:
            raise ValidationFailedException("validation of username failed")

        self.db.put({"email": self.email, "password": self.password}, new_username)
        self.db.delete(self.username)
        self.username = new_username

    def update_email(self, new_email: str) -> None:
        if validate_email(new_email) is False:
            raise ValidationFailedException("validation of email failed")

        self.db.put({"email": new_email, "password": self.password}, self.username)
        self.email = new_email

    def update_password(self, new_password: str) -> None:
        if validate_password(new_password) is False:
            raise ValidationFailedException("validation of password failed")

        hpass = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        self.db.put(
            {
                "email": self.email,
                "password": hpass
            },
            self.username
        )
        self.password = hpass


class UserEmail:
    def __init__(self, db: Deta.Base, email: str, password: str):
        self.email = email
        self.password = password
        self.db = db

    def update_email(self, new_email: str) -> None:
        if self.db.get(new_email) is not None:
            raise UserExistsException()

        if validate_email(new_email) is False:
            raise ValidationFailedException("validation of email failed")

        self.db.put({"password": self.password}, new_email)
        self.db.delete(self.email)
        self.email = new_email

    def update_password(self, new_password: str) -> None:
        if validate_password(new_password) is False:
            raise ValidationFailedException("validation of password failed")

        hpass = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        self.db.put(
            {
                "password": hpass
            },
            self.email
        )
        self.password = hpass
