import requests
from datetime import datetime
from geopy.distance import geodesic
import smtplib
from email.mime.text import MIMEText

# https://www.latlong.net/
# London, UK
my_lat = 51.509865
my_long = -0.118092

# https://proton.me/support/smtp-submission
# https://medium.com/@python_geeks/how-to-send-email-with-python-8770cb33998d
subject = "TEST"
body = """This is the body of 
the text message"""
sender = "wx2ffray5ficr8sh46fr@proton.me"
recipients = ["celeryexchange@gmail.com", "wx2ffray5ficr8sh46fr@gmail.com"]
password = "gsK!888LqERrzb9#"


# check if two coordinates  close to my position
def is_iss_close():
    """
    Checks if the ISS is close.
    """
    # http://open-notify.org/Open-Notify-API/ISS-Location-Now/
    url = "http://api.open-notify.org/iss-now.json"
    r = requests.get(url)
    # raise an exception if call to endpoint not successful
    r.raise_for_status()

    data = r.json()
    iss_latitude = float(data['iss_position']['latitude'])
    iss_longitude = float(data['iss_position']['longitude'])
    iss_position = (iss_latitude, iss_longitude)

    return geodesic(iss_position, (my_lat, my_long)).km < 200


def is_night_time():
    """
    Determines if the current time falls within nighttime hours.
    """
    # https://sunrisesunset.io/api/
    url = "https://api.sunrisesunset.io/json"
    payload = {
        "lat": my_lat,
        "lng": my_long,
        "time_format": 24
    }

    r = requests.get(url, params=payload, verify=True)

    # raise an exception if call to endpoint not successful
    r.raise_for_status()

    data = r.json()
    sunrise_hour = int(data["results"]["sunrise"].split(":")[0])
    sunset_hour = int(data["results"]["sunset"].split(":")[0])
    current_hour = datetime.now().hour

    return current_hour >= sunset_hour or sunset_hour < sunrise_hour


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP('smtp.protonmail.ch', 587) as server:
        server.startttls() # secure the connection
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

send_email(subject, body, sender, recipients, password)


if is_iss_close() & is_night_time():
    pass # send me an email

