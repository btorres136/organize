from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import click
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt, style_from_dict)
from pyfiglet import figlet_format
import sys
import time
from halo import Halo
from datetime import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#cc5454 bold',
    Token.Selected: '#00ff00',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: ' #ff00ff',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '#ffff00',
})

click.command()
def main():
    click.echo(click.style(figlet_format("Organize", font="slant"), fg="blue"))
    click.echo("\tby Brian Torres \n")

    questions = [
        {
            'type': 'list',
            'name': 'Options',
            'message': 'What do you want to do?',
            'choices': [
                {
                    'name': '📅 Add Event',
                    'value': 1
                },
                {
                    'name': '🔊 Add Notification',
                    'value': 2
                },
                {
                    'name': '🎓 Add Class',
                    'value': 3
                }
            ]
        }
    ]
    readOptions(prompt(questions, style=style)['Options'])
    pass


def readOptions(ans):
    options = {
        1: addEvent,
        2: addNotification,
        3: addClassInfo
    }
    return options.get(ans)()

def addClassInfo():
    print('hello')

def addNotification():
    print("👨‍💻 on Development")


def addEvent():

    spinner = Halo(text='Connecting to Google API', spinner='dots')
    spinner.start()
    creds = None

    if os.path.exists('/home/btorres136/UAGM/organize/token.pickle'):
        with open('/home/btorres136/UAGM/organize/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/btorres136/UAGM/organize/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('/home/btorres136/UAGM/organize/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


    # Call the Calendar API
    spinner.stop_and_persist('🦄')

    questions = [
        {
            'type': 'input',
            'name': 'Summary',
            'message': 'Summary:',
        },
        {
            'type': 'input',
            'name': 'location',
            'message': 'location:',
            'default': ''
        },
        {
            'type': 'input',
            'name': 'startDate',
            'message': 'Starting Date:',
            'default': str(datetime.now().day)
        },
        {
            'type': 'input',
            'name': 'startMonth',
            'message': 'Starting Month:',
            'default': str(datetime.now().month)
        },
        {
            'type': 'input',
            'name': 'startYear',
            'message': 'Starting Year:',
            'default': str(datetime.now().year)
        },
         {
            'type': 'input',
            'name': 'endDate',
            'message': 'Ending Date:',
            'default': str(datetime.now().day)
        },
        {
            'type': 'input',
            'name': 'endMonth',
            'message': 'Ending Month:',
            'default': str(datetime.now().month)
        },
        {
            'type': 'input',
            'name': 'endYear',
            'message': 'Ending Year:',
            'default': str(datetime.now().year)
        },
        {
            'type': 'input',
            'name': 'startTime',
            'message': 'Starting Time(24hr):',
        },
        {
            'type': 'input',
            'name': 'endingTime',
            'message': 'Ending Time(24hr):',
        }
    ]
    click.echo(click.style("Provide the following information about the event -> ", fg="green"))
    ans = prompt(questions, style=style)
    event = {
        'summary': ans['Summary'],
        'location': ans['location'],
        'start': {
            'dateTime': ans['startYear']+'-'+ans['startMonth']+'-'+ans['startDate']+'T'+ans['startTime']+':00',
            'timeZone': 'America/Puerto_Rico',
        },
        'end': {
            'dateTime': ans['endYear']+'-'+ans['endMonth']+'-'+ans['endDate']+'T'+ans['endingTime']+':00',
            'timeZone': 'America/Puerto_Rico',
        },
        'reminders': {
            'useDefault': True,
        },
    }
    spinner = Halo(text='Updating Events', spinner='dots')
    spinner.start()
    event = service.events().insert(calendarId='primary', body=event).execute()
    spinner.stop_and_persist('✔')
    print('Event created: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    main()
