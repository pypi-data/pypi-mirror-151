class Magic:
    def __init__(self, db, mlid: str, email: str, name: str):
        self.db = db
        self.mlid = mlid
        self.email = email
        self.name = name

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email
