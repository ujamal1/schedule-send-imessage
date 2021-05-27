from pyicloud import PyiCloudService
from py_imessage import imessage
import applescript
from time import sleep
from datetime import datetime, timedelta, time
import os



def schedule_send():
    firstInput = input("Enter First Name: ").split()
    lastInput = input("Enter Last Name: ").split()
    first = None
    last = None
    target = None

    for c in api.contacts.all():
        if c["firstName"] != None:
            if (c["firstName"] == firstInput[0]) or ((c["firstName"] == firstInput[0]) and (c["lastName"] == lastInput[0])) :
                target = c
                first = firstInput
                break
    print("Found person: " , target["firstName"] + " " + target['lastName'])
    phone = target['phones'][0]['field']
    msg = input("Enter Message: " ).split()
    message = ""
    for i in msg:
        message = message + i + " "
    when = input("Do you want to send this now?(y/n): ")
    if when == "n":
        mins = int(input("In how many minutes do you want to send this message: "))
        current = datetime.now()
        current_td = timedelta(hours=current.hour, minutes=current.minute, seconds=current.second)
        newTime = current + timedelta(minutes= mins)
        newTime_td = timedelta(hours=newTime.hour, minutes= newTime.minute, seconds=current.second)
        checktime = datetime.now()
        checktime_td = timedelta(hours=checktime.hour, minutes=checktime.minute, seconds=current.second)
        print(checktime_td)
        while checktime_td != newTime_td:
            sleep(1)
            checktime = datetime.now()
            checktime_td = timedelta(hours=checktime.hour, minutes=checktime.minute, seconds=checktime.second)
            print(checktime_td)
        print("About to send")
        os.system('osascript sendMessage.applescript "' + phone + '" "' + message + '"')
        print("Sent")

    else:
        os.system('osascript sendMessage.applescript "' + phone + '" "' + message + '"')



def authenticate():
    if api.requires_2fa:
        print("Two-factor authentication required.")
        code = input("Enter the code you received of one of your approved devices: ")
        result = api.validate_2fa_code(code)
        print("Code validation result: %s" % result)

        if not result:
            print("Failed to verify security code")
            sys.exit(1)

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
            print("  %s: %s" % (i, device.get('deviceName', "SMS to %s" % device.get('phoneNumber'))))

        device = click.prompt('Which device would you like to use?', default=0)
        device = devices[device]
        if not api.send_verification_code(device):
            print("Failed to send verification code")
            sys.exit(1)

        code = click.prompt('Please enter validation code')
        if not api.validate_verification_code(device, code):
            print("Failed to verify verification code")
            sys.exit(1)


if __name__ == '__main__':
    api = PyiCloudService(#Enter icloud username-> "" ,Enter icloud password -> "")
    authenticate()
    schedule_send()

