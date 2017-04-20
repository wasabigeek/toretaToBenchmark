import requests
import datetime
import fnmatch
import os
import shutil

from bs4 import BeautifulSoup

import config


def archive_old_csvs():
    rootPath = config.TORETA_RAW_DATA_DIR
    destDir = config.ARCHIVES_DIR

    matches = []
    for root, dirnames, filenames in os.walk(rootPath):
        for filename in fnmatch.filter(filenames, '*.csv'):
            matches.append(os.path.join(root, filename))
            shutil.move(
                os.path.join(root, filename),
                os.path.join(destDir, filename)
            )

    print('Archiving from', rootPath, ":", matches)


def login(session, login_url, email, password):

    # get authenticity_token from hidden input
    LOGIN_URL = login_url
    response = session.get(LOGIN_URL)

    soup = BeautifulSoup(response.text, "html.parser")
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
def download_file(session, download_url, venue):
    # NOTE the stream=True parameter
    r = session.get(download_url, stream=True)
    timestamp = datetime.datetime.now().strftime("%Y%b%d_%Hh%Mm%Ss")
    filename = '{venue}_toreta_{timestamp}.csv'.format(
        venue=venue,
        timestamp=timestamp
    )
    path_to_file = '{toreta_dir}/{venue}/{filename}'.format(
        toreta_dir=config.TORETA_RAW_DATA_DIR,
        venue=venue,
        filename=filename
    )
    with open(path_to_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                # f.flush() commented by recommendation from J.F.Sebastian
    return path_to_file


def login_and_download():
    for account in config.TORETA_ACCOUNTS:
        s = requests.Session()

        login(
            session=s,
            login_url=account['login_url'],
            email=account['email'],
            password=account['password'],
        )
        print('Downloading from {}'.format(account['download_url']))
        download_file(
            session=s,
            download_url=account['download_url'],
            venue=account['venue']
        )
