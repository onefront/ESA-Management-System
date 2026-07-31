import os
from urllib.parse import quote_plus


class Config:
    SECRET_KEY = "esa_secret_key_2026"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    # Detect PythonAnywhere
    if "PYTHONANYWHERE_SITE" in os.environ:

        password = quote_plus("Property@4848")

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://onefront:{password}"
            "@onefront.mysql.pythonanywhere-services.com/onefront$esa_db"
        )

    # Local Windows development
    else:

        password = quote_plus("Property@4848")

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://root:{password}"
            "@localhost/esa_db"
        )

        # ==========================
        # Hubtel SMS Configuration
        # ==========================

        HUBTEL_CLIENT_ID = ""

        HUBTEL_CLIENT_SECRET = ""

        HUBTEL_SENDER_ID = "ESA"