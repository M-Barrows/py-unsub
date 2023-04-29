from __future__ import print_function

import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from lib import  get_header,  get_unsub_links, parse_link
from alive_progress import alive_bar
import pprint


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_emails(max_fetch:int=10):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId="me",maxResults=max_fetch,q="is:unread unsubscribe").execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
            return
        sender_dict = dict()
        with alive_bar(len(messages),bar="filling") as bar:
            for i, message in enumerate(messages,1):
                message_obj = service.users().messages().get(userId="me",id = message['id'], format="full").execute()
                unsub = get_unsub_links(message_obj)
                sender = parse_link(get_header(message_obj,"From"))
                if not sender_dict.get(sender):
                    sender_dict.update({sender:list()})
                if unsub not in sender_dict.get(sender) and unsub != 'None':
                    sender_dict.get(sender).append(unsub)
                bar()
        sender_dict = {key:val for key,val in sender_dict.items() if val != ['None'] and val != []}
        print(len(sender_dict.keys()))
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
    return sender_dict

