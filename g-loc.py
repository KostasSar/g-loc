from ast import arg
import os.path

import re

from time import sleep

import argparse
from urllib.request import ProxyDigestAuthHandler

from apiclient import discovery

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/contacts']



banner = """
 .d8888b.         888                   
d88P  Y88b        888                   
888    888        888                   
888               888  .d88b.   .d8888b 
888  88888        888 d88""88b d88P"    
888    888 888888 888 888  888 888      
Y88b  d88P        888 Y88..88P Y88b.    
 "Y8888P88        888  "Y88P"   "Y8888P                                              
                                                      
"""



def cmdline_args():
    description_text = """
    Google account activity locator. 
    """
    epilog_text = """

    Options --email and --txtfile are mutually exclusive.

    Example of use:
        python g-loc.py -e foobar@gmail.com
                    or
        python g-loc.py -t mail_list.txt -o output.txt 
        \n
    """

    parser = argparse.ArgumentParser(prog="g-loc",
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description=description_text,
                                    epilog=epilog_text)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', "--email", action='store', 
                        help="search given email")
    group.add_argument('-t', "--txtfile", action='store',
                        help="search each mail in the text file. One mail per line.")
    parser.add_argument('-o', "--output", action='store',
                        help="output file", required=False)
    parser.add_argument('-b', "--banner", action="store_true", default=False,
                        help="hide banner")
    # parser.add_argument('-v', "--verbosity", type=int, choices=[0,1,2], default=0, 
    #                    help="increase output verbosity (default: %(default)s)")
    
    return(parser.parse_args())



def get_authorisation():
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
    return creds



def valid_mail_format(mail):
    mail_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if(re.fullmatch(mail_regex, mail)):
        return True
    else:
        return False



def add_contact(service, mail):
    if valid_mail_format(mail):
        name = mail.split('@')[0]
        # print(name + "   " + mail)
        service.people().createContact( body={
            "names": [
                {
                    "givenName": name
                }
            ],
            "emailAddresses": [
                {
                    'value': mail
                }
            ]
        }).execute()
        print("Added " + name + " to contacts.")
    elif len(mail.strip()) == 0:
        # Ignore empty line
        return False
    else:
        print("Address invalid, skipping " + mail)
        return False



def list_contact_info(service, input, output_file):
    try:
        # Call the People API
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=1000,
            personFields='names,emailAddresses,metadata').execute()
        connections = results.get('connections', [])

        # Collects each contact's resource name to pass them to the delete_contact function and cleanup
        resource_names = []

        for person in connections:

            # emailAddresses returns a list containing a dictionary including 
            # an element called "value" which contains the contact's mail.
            person_mail_dict = person.get('emailAddresses', [])[0] 
            mail = person_mail_dict['value']
            
            if mail not in input:
                continue

            resource_names.append(person.get("resourceName"))

            names = person.get('names', [])
            if names:
                print("-"*60, file=output_file)
                name = names[0].get('displayName')
                print(name, file=output_file)

                #Prints Google ID
                metadata = person.get('metadata', [])
                profileData = metadata.get('sources', [])
                try:
                    sources = profileData[1]
                except IndexError:
                    print("No Google account for " + name, file=output_file)
                    continue
                id = sources.get('id', [])

                # Usually the first part of the email address is included in the 
                # user's YouTube channel link and is used as the channel's default name
                yt_chan = mail.split('@')[0]

                
                # If no output file is not specified (has None value), 
                # sys.stdout will be used insted.

                # Prints Google ID
                print("Google account ID:", file=output_file)
                print(id + "\n", file=output_file)

                # Prints Google Photos link
                #       https://get.google.com/albumarchive/{userID}
                print("Google photo album:", file=output_file)
                print("https://get.google.com/albumarchive/" + id + "\n", file=output_file)

                # Prints Maps contributions link
                #       https://www.google.com/maps/contrib/{userID}
                print("Google maps activity:", file=output_file)    
                print("https://www.google.com/maps/contrib/" + id + "\n", file=output_file)

                # Prints user's link to YouTube channel
                print("YouTube channel:", file=output_file)
                print("https://www.youtube.com/user/" + yt_chan + "\n", file=output_file)

    except HttpError as err:
        print(err)
    
    return resource_names


def delete_contact(service, resource_name):
    try:
        service.people().deleteContact(resourceName=resource_name).execute()
    except HttpError as err:
        print(err)


def main():
    """
    Gets access to executing user's Google Contacts.
    Creates target contacts.
    Locates their activity and outputs links to it.
    Deletes contacts to avoid clutter.
    """
    
    args = cmdline_args()

    hide_banner = args.banner
    if not hide_banner:
        print(banner)
    
    creds = get_authorisation()

    try:
        service = build('people', 'v1', credentials=creds)
    except HttpError as err:
        print(err)

    if args.email:
        print("Searching single mail address:\n")
        mail = args.email.strip()
        add_contact(service, mail)
        input = mail
    elif args.txtfile:
        print("Using provided .txt file for mail input:\n")
        mail_file = open(args.txtfile)
        mail_list = mail_file.read().splitlines()
        for mail in mail_list:
            add_contact(service, mail)
        input = mail_list
        

    print("Added contacts, locating activity...")
    sleep(15)

    # If no output file is specified, output_file is assigned as None.
    if args.output:
        output_file = open(args.output, 'w')
    else:
        output_file = None

    resource_names = list_contact_info(service, input, output_file)
    
    for contact in resource_names:
        delete_contact(service,contact)
    
    # print("Deleted target contacts to avoid clutter.")



if __name__ == '__main__':
    main()

