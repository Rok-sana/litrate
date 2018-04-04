import enum

DATABASE_CONFIG = {"user": "root",
                   "password": "123456",
                   "database": "litrate",
                   "host": "127.0.0.1"}
SECRET_KEY = "verysecretkey"


class USER_TYPES():
    PUBLISHER = "Publisher"
    CREATOR = "Creator"
    MODERATOR = "Moderator"
