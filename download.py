from bs4 import BeautifulSoup
import requests
import datetime


def login(session, login_url, email, password):

    # get authenticity_token from hidden input
    LOGIN_URL = login_url
    response = session.get(LOGIN_URL)

    soup = BeautifulSoup(response.text)
    auth_input = soup.find(attrs={"name": "authenticity_token"})
    auth_token = auth_input.get('value')

    # login
    session.post(
        LOGIN_URL,
        {
            'email': email,
            'password': password,
            'authenticity_token': auth_token,
        }
    )


# download relevant CSV
def download_file(session, download_url, folder_name):
    # NOTE the stream=True parameter
    r = session.get(download_url, stream=True)
    timestamp = datetime.datetime.now().strftime("%Y%b%d_%Hh%Mm%Ss")
    local_filename = '{0}/customers_{1}.csv'.format(
        folder_name,
        timestamp
    )
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                # f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


# RUNTIME
from secret import toreta_accounts

for account in toreta_accounts:
    s = requests.Session()

    login(
        session=s,
        login_url=account['login_url'],
        email=account['email'],
        password=account['password'],
    )
    download_file(
        session=s,
        download_url=account['download_url'],
        folder_name=account['folder_name']
    )
