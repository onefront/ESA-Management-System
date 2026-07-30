from urllib.parse import quote_plus

class Config:
    SECRET_KEY = "esa_secret_key_2026"

    password = quote_plus("YOUR_LOCAL_MYSQL_PASSWORD")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://root:{password}@localhost/esa_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }