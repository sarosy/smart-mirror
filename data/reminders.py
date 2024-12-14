from dotenv import load_dotenv
import os
import pyicloud

class Reminders:
    def __init__(self):
       # Authenticate to iCloud
        self.api = self.apple_authenticate()

    def fetch_reminders(self):
        pass

    def apple_authenticate(self):

        # Get email and pwd from env variables
        load_dotenv()
        email = os.getenv("APPLE_EMAIL")
        pwd = os.getenv("APPLE_PWD")

        # Authenticate with email and password
        api = pyicloud.PyiCloudService(email, pwd)
        # Erase email and pwd env vars so they don't persist as mirror runs
        os.environ.pop("APPLE_EMAIL", None)
        os.environ.pop("APPLE_PWD", None)

        if api.requires_2fa:
            print("Two-factor authentication required.")
            code = input("Enter the code you received of one of your approved devices: ")
            result = api.validate_2fa_code(code)
            print("Code validation result: %s" % result)

            if not result:
                print("Failed to verify security code")
                return None

            if not api.is_trusted_session:
                print("Session is not trusted. Requesting trust...")
                result = api.trust_session()
                print("Session trust result %s" % result)

                if not result:
                    print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
        elif api.requires_2sa:
            import click
            print("Two-step authentication required. Your trusted devices are:")

            devices = api.trusted_devices
            for i, device in enumerate(devices):
                print(
                    "  %s: %s" % (i, device.get('deviceName',
                    "SMS to %s" % device.get('phoneNumber')))
                )

            device = click.prompt('Which device would you like to use?', default=0)
            device = devices[device]
            if not api.send_verification_code(device):
                print("Failed to send verification code")
                return None

            code = click.prompt('Please enter validation code')
            if not api.validate_verification_code(device, code):
                print("Failed to verify verification code")
                return None
        
        return api
