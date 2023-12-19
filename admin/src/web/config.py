import os


class Config:
    """ Base configuration """
    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"

    JWT_SECRET_KEY = "secret_key"
    JWT_TOKEN_LOCATION = ["json", "headers"]

    # Credenciales para envio de emails
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = "code.guess2022@gmail.com"
    MAIL_PASSWORD = "vheu bwqc lven nysz"
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False

    # Credenciales para registro con google
    GOOGLE_CLIENT_ID = "1036650896074-fhkr6mj471n2q1p1q8j7jepn1re9lg6b.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "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"


class ProductionConfig(Config):
    """ Production configuration """

    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )


class DevelopmentConfig(Config):
    """ Development configuration """

    DB_USER = "grupo15"
    DB_PASS = "123"
    DB_HOST = "localhost"
    DB_NAME = "grupo15_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
}
