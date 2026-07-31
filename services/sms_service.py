import requests
from flask import current_app


class SMSService:
    """Hubtel SMS Service"""

    @staticmethod
    def send_sms(recipient, message):
        """
        Sends an SMS through Hubtel.

        Returns:
            dict:
                {
                    "success": True/False,
                    "response": ...
                }
        """

        client_id = current_app.config.get("HUBTEL_CLIENT_ID")
        client_secret = current_app.config.get("HUBTEL_CLIENT_SECRET")
        sender = current_app.config.get("HUBTEL_SENDER_ID")

        # Credentials not configured yet
        if not client_id or not client_secret:
            return {
                "success": False,
                "response": "Hubtel credentials not configured."
            }

        url = "https://smsc.hubtel.com/v1/messages/send"

        params = {
            "clientid": client_id,
            "clientsecret": client_secret,
            "from": sender,
            "to": recipient,
            "content": message
        }

        try:
            response = requests.get(url, params=params, timeout=30)

            return {
                "success": response.status_code == 200,
                "response": response.json()
            }

        except Exception as e:
            return {
                "success": False,
                "response": str(e)
            }