import bcrypt
import deta

from ..errors import ValidationFailedException, UserExistsException, UserNotFoundException, InvalidPasswordException
from ..models.user import UserEmail, User
from ..validation import validate_username, validate_email, validate_password


class OAuth:
    def __init__(self, deta_key: str, db_name: str, email_as_username: bool = False, validation: bool = True):
        deta_ = deta.Deta(deta_key)
        self.db = deta_.Base(db_name)
        self.validation = validation

        self.sign_up = self.sign_up if not email_as_username else self.sign_up_email
        self.sign_in = self.sign_in if not email_as_username else self.sign_in_email

    def sign_up(self, username: str, email: str, password: str) -> User:
        if self.db.get(username) is not None:
            raise UserExistsException(f"{username} already exists")

        if self.validation:
            if False in [validate_username(username), validate_email(email), validate_password(password)]:
                raise ValidationFailedException(f"validation failed for any one of the fields")

        hpass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.db.put({"email": email, "password": hpass.decode()}, username)
        return User(self.db, email, username, hpass.decode())

    def sign_up_email(self, email: str, password: str) -> UserEmail:
        if self.db.get(email) is not None:
            raise UserExistsException(f"{email} already exists")

        if self.validation:
            if False in [validate_email(email), validate_password(password)]:
                raise ValidationFailedException("validation failed for any one of the fields")

        hpass = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.db.put({"password": hpass}, email)
        return UserEmail(self.db, email, hpass.decode())

    def sign_in(self, username: str, password: str) -> User:
        user = self.db.get(username)
        if user is None:
            raise UserNotFoundException(f"{username} does not exist")

        if bcrypt.checkpw(password.encode(), user["password"].encode()):
            return User(self.db, user["email"], user["key"], user["password"])
        raise InvalidPasswordException()

    def sign_in_email(self, email: str, password: str) -> UserEmail:
        user = self.db.get(email)
        if user is None:
            raise UserNotFoundException(f"{email} does not exist")

        if bcrypt.checkpw(password.encode(), user["password"].encode()):
            return UserEmail(self.db, user["key"], user["password"])
        raise InvalidPasswordException()
