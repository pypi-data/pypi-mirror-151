import smtplib
import uuid
import warnings

import deta

from ..errors import LinkExpiredException, IncorrectEmailException
from ..models.magic import Magic


class NotDefaultPortWarning(Warning):
    pass


BASE = """From: {} <{}>
To: {} <{}>
Content-Type: text/html
Subject:{}
<h1>{}</h1>
<a href="{}">Click here</a> to sign in to <strong>{}</strong>
"""


class MagicLink:
    def __init__(
            self,
            deta_key: str,
            db_name: str,
            host: str,
            port: int,
            email: str,
            password: str,
            org: str,
            domain: str,
            expiry: int = 900,
            name: str = ""
    ):
        if port not in [110, 995, 143, 993, 25, 26, 465, 587]:
            warnings.warn(f"port '{port}' is not one of the default ports used by mail servers")

        self.deta_ = deta.Deta(deta_key)
        self.db = self.deta_.Base(db_name)
        self.host = host
        self.port = port
        self.email = email
        self.password = password
        self.name = str(name)
        self.org = org
        self.domain = domain
        self.expiry = expiry
        self.smtp = smtplib.SMTP(self.host, self.port)

    def send_email(self, email: str, name: str = "") -> None:
        mlid = str(uuid.uuid4())
        self.db.put({"email": email, "name": name}, mlid, expire_in=self.expiry)
        email_msg = BASE.format(
            self.name,
            self.email,
            name,
            email,
            f"Link to Sign In to {self.org}",
            self.org,
            self.domain + mlid + "?email=" + email + "?name=" + name,
            self.org
        )
        self.smtp.send(email_msg)

    def validate_link(self, mlid: str, email: str, name: str) -> Magic:
        ml = self.db.get(mlid)
        if ml is None:
            raise LinkExpiredException("link has either expired or doesnt exist")

        if ml["email"] != email:
            raise IncorrectEmailException("email for link and given email does not match")

        return Magic(self.db, mlid, email, name)
