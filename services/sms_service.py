import requests

from models.sms_setting import SMSSetting


class SMSService:

    @staticmethod
    def send_sms(phone, message):

        settings = SMSSetting.query.filter_by(
            is_active=True
        ).first()

        if not settings:
            return False, "SMS Settings not configured."

        url = f"{settings.base_url}?key={settings.api_key}"

        payload = {
            "recipient": [phone],
            "sender": settings.sender_id,
            "message": message,
            "is_schedule": False,
            "schedule_date": ""
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:

            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )

            result = response.json()

            if response.status_code == 200:
                return True, result

            return False, result

        except Exception as e:

            return False, str(e)