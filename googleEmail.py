#!/usr/bin/env python
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from email.mime.base import MIMEBase
import base64
from email.message import EmailMessage

import os
import httplib2

class googleEmailApi:
    def __init__(self):
        try:
            import argparse
            self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            self.flags = None

        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/gmail-python-quickstart.json
        self.SCOPES = 'https://mail.google.com/'#'https://www.googleapis.com/auth/gmail.send'
        self.CLIENT_SECRET_FILE = 'credentials.json'
        self.APPLICATION_NAME = 'Gmail API Python Quickstart'
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=http)


    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def create_message(self, sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        body = {'raw': raw}
        #print(body)
        return(body)
        #return {'raw': base64.urlsafe_b64encode(message.as_bytes())}


    def send_message(self, user_id, message):
        message = (self.service.users().messages().send(userId=user_id, body=message).execute())
        return message

    def create_message_with_attachment(self,sender, to, subject, message_text, file):
        mime_message = EmailMessage()
        mime_message['to'] = to
        mime_message['from'] = sender
        mime_message['subject'] = subject
        # text
        mime_message.set_content(
            'Hi, below is the quotation file.'
            'Kindly check it.'
        )
        attachment_filename = f"{file}"
        print(attachment_filename)
        type_subtype, _ = mimetypes.guess_type(attachment_filename)
        maintype, subtype = type_subtype.split('/')
        with open(attachment_filename, 'rb') as fp:
            attachment_data = fp.read()
        filename = file.split("/")
        filename = filename[-1]
        mime_message.add_attachment(attachment_data, maintype, subtype, filename=filename)
        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
        return {'raw': encoded_message}







