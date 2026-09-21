# import os
# from urllib.parse import quote_plus
#
#
# class Config:
#     SECRET_KEY = "esa_secret_key_2026"
#
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#     SQLALCHEMY_ENGINE_OPTIONS = {
#         "pool_pre_ping": True,
#         "pool_recycle": 280,
#     }
#
#     # Detect PythonAnywhere
#     if "PYTHONANYWHERE_SITE" in os.environ:
#
#         password = quote_plus("Property@4848")
#
#         SQLALCHEMY_DATABASE_URI = (
#             f"mysql+pymysql://onefront:{password}"
#             "@onefront.mysql.pythonanywhere-services.com/onefront$esa_db"
#         )
#
#     # Local Windows development
#     else:
#
#         password = quote_plus("Property@4848")
#
#         SQLALCHEMY_DATABASE_URI = (
#             f"mysql+pymysql://root:{password}"
#             "@localhost/esa_db"
#         )
#
#         # ==========================
#         # Hubtel SMS Configuration
#         # ==========================
#
#         HUBTEL_CLIENT_ID = ""
#
#         HUBTEL_CLIENT_SECRET = ""
#
#         HUBTEL_SENDER_ID = "ESA"
#
# class Config:
#     SECRET_KEY = os.environ.get("SECRET_KEY", "")
#
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_ENGINE_OPTIONS = {
#         "pool_pre_ping": True,
#         "pool_recycle": 280
#     }
#
#     # Paystack
#     PAYSTACK_SECRET_KEY = os.environ.get("PAYSTACK_SECRET_KEY", "")
#     PAYSTACK_PUBLIC_KEY = os.environ.get("PAYSTACK_PUBLIC_KEY", "")
#     PAYSTACK_CALLBACK_URL = os.environ.get(
#         "PAYSTACK_CALLBACK_URL",
#         "https://onefront.pythonanywhere.com/member-payments/paystack/callback"
#     )
#
#     # your existing database configuration continues here



import os
from urllib.parse import quote_plus


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "esa-connect-local-development-secret-key-2026"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280
    }

    # =========================
    # PAYSTACK CONFIGURATION
    # =========================

    PAYSTACK_SECRET_KEY = os.environ.get(
        "PAYSTACK_SECRET_KEY",
        ""
    )

    PAYSTACK_PUBLIC_KEY = os.environ.get(
        "PAYSTACK_PUBLIC_KEY",
        ""
    )

    PAYSTACK_CALLBACK_URL = os.environ.get(
        "PAYSTACK_CALLBACK_URL",
        "http://127.0.0.1:5000/member-payments/paystack/callback"
    )







      # =========================
    # DATABASE CONFIGURATION
    # =========================

    if "PYTHONANYWHERE_SITE" in os.environ:
        password = quote_plus("YOUR_DATABASE_PASSWORD")

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://onefront:{password}"
            "@onefront.mysql.pythonanywhere-services.com/"
            "onefront$esa_db"
        )


    else:

        password = quote_plus("Property@4848")

        SQLALCHEMY_DATABASE_URI = (

            f"mysql+pymysql://root:{password}"

            "@localhost/esa_db"

        )

    # =========================
    # EXISTING HUBTEL SETTINGS
    # =========================

    HUBTEL_CLIENT_ID = os.environ.get(
        "HUBTEL_CLIENT_ID",
        ""
    )

    HUBTEL_CLIENT_SECRET = os.environ.get(
        "HUBTEL_CLIENT_SECRET",
        ""
    )

    HUBTEL_SENDER_ID = os.environ.get(
        "HUBTEL_SENDER_ID",
        "ESA"
    )