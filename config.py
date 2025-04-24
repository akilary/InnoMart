import os


DIR_PATH = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(f"{DIR_PATH}/data", "InnoMartDB.db")


class Config:
    SECRET_KEY = "super-secret-key-12345"
    DATABASE = DATABASE_PATH
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
