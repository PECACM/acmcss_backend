import json
import os

import requests
from background_task import background
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string
from dotenv import load_dotenv

from events.models import Event
from acmcss.settings import BASE_DIR

dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)


@background(schedule=3)
def registration_user_notify(event_id, username):
    print("Registration notification process started")

    user = User.objects.get(username__exact=username)
    event = Event.objects.get(id=event_id)
    email = user.email
    name = user.first_name + " " + user.last_name
    time = event.dateTime
    location = event.locations

    merge_data = {
        'name': name,
        'username': username,
        'event_name': event.name,
        'event_time': time,
        'event_location': location,
    }

    try:
        subject = render_to_string("event_registration/message_subject.txt", merge_data)
        text_body = render_to_string("event_registration/message_body.txt", merge_data)
        html_body = render_to_string("event_registration/message_body.html", merge_data)

        msg = EmailMultiAlternatives(subject=subject, from_email=os.getenv('EMAIL_HOST_USER'),
                                     to=[email], body=html_body)
        msg.attach_alternative(html_body, "text/html")
        msg.send()

        print("mail successfully send to " + email)

    except Exception as e:
        print(e)
        print("Some error occurred while sending mail to " + email)


@background(schedule=2)
def eventbeep_api(event_id, username):
    print("Post Request to EventBeep Started")
    user = User.objects.get(username__exact=username)
    eventbeep_url = 'https://api.eventbeep.com/newRegistration'

    payload = {
        "eventID": str(event_id),  # event_id
        "name": user.first_name + " " + user.last_name,
        "email": user.email,
        "phoneNumber": str(user.participant.contactNumber)
    }

    json_payload = json.dumps(payload)

    headers = {'Content-type': 'application/json'}
    status = requests.post(eventbeep_url, data=json_payload, headers=headers)
    print("Status: " + str(status.text))
    print("Notification Sent Successfully")


@background(schedule=2)
def new_user_notify(username):
    user = User.objects.get(username__exact=username)
    email = user.email

    body = """
    Hello there,
    Greetings from PECFest'19!
    Thank you for joining PECFest family. 
    A festival, a show, a brand, it has many facets. It's more than the thumping heartbeats of 50,000 people.
    It's PECFest - the biggest techno-cultural festival in North India! Year after year we've made memories, and 
    there's more to come. Scaling new heights with each edition, PECFest 2019 promises to deliver nothing but the best.
    
    You can use your unique PECFest ID {username}, to register for events at pecfest.in/events
    For more information including about our Cultural and Star Nights, stay tuned at pecfest.in
    
    For all the latest updates, connect with us on : 
    Facebook : facebook.com/pecfestofficial
    Instagram : instagram.com/pec.pecfest
    
    Contact us at : pecfest.in/team
    
    See you there! 
    
    PECFest 2019
    """.format(name=user.first_name, username=username)

    try:
        send_mail(
            'Welcome to PECFEST 2019',
            body,
            os.getenv('EMAIL_HOST_USER'),
            [email],
            fail_silently=False,
        )
        print("mail successfully send to " + email)
    except Exception as e:
        print("Some error occurred while sending mail to " + email)
