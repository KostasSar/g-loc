# G-loc

```
 .d8888b.         888                   
d88P  Y88b        888                   
888    888        888                   
888               888  .d88b.   .d8888b 
888  88888        888 d88""88b d88P"    
888    888 888888 888 888  888 888      
Y88b  d88P        888 Y88..88P Y88b.    
 "Y8888P88        888  "Y88P"   "Y8888P  
```

G-loc is a python tool that locates a user's Google account activity just by providing the account's email.

Activity output includes:
- Google Maps reviews and photos
- Google Photos
- Google Account ID
- YouTube channel

Input can be either a simgle email address or a .txt file containing up to 1000 addresses in separate lines and the output can either be printed on the terminal or redirected to an output file.

In short, Python is used to contact Google contacts and the People API. 

In further detail, each given email is used to create a new Google contact in the executing user's Google Contacts account. Then by listing these contacts, metadata is extracted to identify, by Google ID, and locate each target account's activity on Google Photos, Google Maps and the target user's YouTube channel. Please note that since Youtube channels can have modified names, double check if the account in the output actually belongs to the target user, as only default YouTube channels use the first part of the Gmail as the channel name. Finally, all new target contacts are deleted to avoid clutter in the executing user's Google Contacts account.

It inspired by the Hack the Box, now retired, OSINT challenge "ID Exposed" where the objective is to locate the target "Sara Medson Cruz" only from her gmail account and automates the actions taken to find the Google account id and locate the activty that contains the flag. 



## Table of Contents
- [G-loc](#g-loc)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
  - [Usage](#usage)
  - [Troubleshooting](#troubleshooting)
  - [TODOs](#todos)
  - [HTB Challenge ID Exposed write-up](#htb-challenge-id-exposed-write-up)
    - [Case:](#case)
    - [Manual Solution:](#manual-solution)
    - [G-loc Solution:](#g-loc-solution)
  - [Author](#author)
  - [Resources](#resources)
  - [License](#license)



## Setup 


To work with Google’s API and services, install the Google API Client and Authentication Library.

Run command:

```bash
pip install — upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

To setup Google Credentials in Google Cloud Platform visit:

    https://console.cloud.google.com/

1. Choose or create Project in Google Console
1. Enable required Google API and Services.

    Enable the services you would like to use from API Library. You can find it through API and Services menu.

    API and Services → Library → Search and Enable the service

    For Contact API: Contact API and People API need to be enabled
    
1. Create OAuth2 Screen Consent

    Before creating OAuth2 credentials, you will need to create OAuth2 Screen Consent where you can add scopes according to the services you will be using.

    You can find Consent Screen through:

    API and Services → OAuth Consent Screen

    - Add App Information
    - Add scopes : Contact API
    - Add test user emails
    - Add other details as required

1. Create Oauth2 Credentials

    API and Services → Credentials → Create OAuth2 creds

    - Choose Application type : WebApp, android or iOS (according to your requirement)
    - Complete setup and it generates : client_secret, client_id
    - During setup: Add Redirect URIs to your created OAuth2 credentials


    Download OAuth2 json credentials in working directory as “credentials.json ”

    Eg. of Generated OAuth2 json

    ```json
    {
        "web": {
            "client_id": <client_id>,
            "project_id": <project_id>,
            "auth_uri": <auth_uri>,
            "token_uri": <token_uri>,
            "auth_provider_x509_cert_url": <auth_provider>,
            "client_secret": <client_secret>,
            "redirect_uris": <list of redirect_uris> 
        }
    }
    ```

    Note: Add credentials.json in .gitignore as it is sensitive information

    Use Redirect URI from credentials.json

    ```
    /* "redirect_uris": ["http://localhost:42047/"] */
    ```
    Note: Match your Redirect URI in OAuth2 client with that of credentials.json

1. (OPTIONAL STEP) Create a virtual environment for this project

1. In the destination directory:
   ```console
    git clone https://github.com/KostasSar/g-loc.git 
   ```

1. Install dependencies from requirements.txt
   ```console
    pip install -r requirements.txt
   ```

1. Run script



## Usage


```console
$ python g-loc.py -h
usage: g-loc [-h] (-e EMAIL | -t TXTFILE) [-o OUTPUT] [-b]

    Google account activity locator. 
    

optional arguments:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        search given email
  -t TXTFILE, --txtfile TXTFILE
                        search each mail in the text file. One mail per line.
  -o OUTPUT, --output OUTPUT
                        output file
  -b, --banner          hide banner

    Options --email and --txtfile are mutually exclusive.

    Example of use:
        python g-loc.py -e foobar@gmail.com
                    or
        python g-loc.py -t mail_list.txt -o output.txt 
        

```


```bash
python g-loc.py -e saramedsoncruz@gmail.com
```
    
or
    
    
```bash
python g-loc.py -t mail_list.txt -o output.txt
```

Example mail_list.txt:
```
saramedsoncruz@gmail.com
test@gmail.com
foobar@gmail.com
```



## Troubleshooting

1. Sometimes the Google API does not return the whole list of the target contacts and as a result the input contacts are not deleted from the executing user's Google Contacts account. 
   
   Solution:
   
   Executing the script again with the same arguments produces some duplicate results but will clean up the remaining contacts left behind by the previous execution.


## TODOs

- Implement verbosity
- Refactor list_contact_info and add a decorator


## HTB Challenge ID Exposed write-up

### Case:

We are looking for Sara Medson Cruz's last location, where she left a message. 
We need to find out what this message is! 
We only have her email: saramedsoncruz@gmail.com

### Manual Solution:

1. No social media profiles at all. Some false positives unrelated to the challenge.
2. Using [Sherlock](https://github.com/sherlock-project/sherlock) social media finding tool got me some more false positives.
3. Since only a google account was available, looked up in Google Maps "local guides" finder. But got no results.
4. Added Sara as a contact to get some more info but there are no google user profiles since G+ was taken down.
5. The challenge's title refers to an ID link. Looked up for Google account IDs. 
6. Inspecting the google contact card code, got a data person ID


    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    data-personid="c6525731637870473784"
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


7. Using this person id into google developer's API people.get and fetching for the “metadata" section of the account we get the google account's ID

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    1*******************4
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


8. Finally, the google account and location hint to a maps post. And by visiting 
    https://www.google.com/maps/contrib/{google id} we get the user's maps contributions.
9. The flag is found in a football museum review  


    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    HTB{i***********************D}
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### G-loc Solution:

1. Provide the target email to g-loc:
![Screenshot of script execution using saramedsoncruz@gmail.com as input](https://i.imgur.com/qhj14i3.png "Locating Sara.")

1. Click on the Google Maps link
1. Find the Gfootball museum review containing the flag.

1. Submit 
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    HTB{i***********************D}
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## Author

Kostas Sarikioses

[LinkedIn](https://www.linkedin.com/in/kostas-sarikioses/)

[Github](https://github.com/KostasSar)

## Resources

- [Getting a Grasp on GoogleID’s](https://sector035.nl/articles/getting-a-grasp-on-google-ids)

- [Keeping a Grip on GoogleID’s](https://sector035.nl/articles/keeping-a-grip-on-google-ids)

- [Google Contact API integration with Python](https://towardsdev.com/google-contact-api-integration-with-python-f9777b97e51d) from [Liza Amatya](https://medium.com/@lizaamatya) for the documentation.

- [HTB Challenge ID Exposed](https://app.hackthebox.com/challenges/id-exposed)

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/#)

