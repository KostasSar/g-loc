```brainfuck # language just to make it look green and pretty 
 .d8888b.         888                   
d88P  Y88b        888                   
888    888        888                   
888               888  .d88b.   .d8888b 
888  88888        888 d88""88b d88P"    
888    888 888888 888 888  888 888      
Y88b  d88P        888 Y88..88P Y88b.    
 "Y8888P88        888  "Y88P"   "Y8888P  
```
# G-loc


G-loc is a python tool that locates a user's Google account activity just by providing the account's email.

Activity output includes:
- Google Maps reviews and photos
- Google Photos
- Google Account ID
- YouTube channel

Input can be either a simgle email address or a .txt file containing up to 1000 addresses in separate lines and the output can either be printed on the terminal or redirected to an output file.

Python is used to contact Google contacts and the People API.

It inspired by the Hack the Box, now retired, OSINT challenge "ID Exposed" where the objective is to locate the target "Sara Medson Cruz" only from her gmail account and automates the actions taken to find the Google account id and locate the activty that contains the flag. 




## Table of Contents
- [G-loc](#g-loc)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
  - [Usage](#usage)
  - [Troubleshooting](#troubleshooting)
  - [TODOs](#todos)
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
   ```bash
    git clone https://github.com/KostasSar/G-loc.git 
   ```

1. Install dependencies from requirements.txt
   ```bash
    pip install -r requirements.txt
   ```

1. Run script



## Usage

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


Execution example screenshot:
![Screenshot of script execution using saramedsoncruz@gmail.com as input](https://i.imgur.com/i62LBzv.png "Locating Sara.")


## Troubleshooting

1. Sometimes the Google API does not return the whole list of the target contacts and as a result the input contacts are not deleted from the executing user's Google Contacts account. 
   
   Solution:
   
   Executing the script again with the same arguments produces some duplicate results but will clean up the remaining contacts left behind by the previous execution.


## TODOs

- Implement verbosity
- Refactor list_contact_info and add a decorator


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

