import os
import csv
import re
import datetime

import config

current_directory = os.path.dirname(os.path.abspath(__file__))

today_str = datetime.datetime.now()
today_str = today_str.strftime('%d%b%Y')

CSV_HEADERS = ['firstname', 'lastname', 'email']


def process_folder(input_folder, file_source, output_paths):

    target_path = input_folder
    csvfiles = [f for f in os.listdir(target_path) if f.endswith('.csv')]

    if not csvfiles:
        print("Couldn't find any CSV files in", target_path, ":(\nMoving on...\n")
        return

    total = 0
    total_edm_contacts = 0
    edm_contacts = []

    row_process_mapping = {
        'toreta': process_toreta_row,
        'camcard': process_camcard_row,
        'chope': process_chope_row,
    }
    process_row_fn = row_process_mapping[file_source]

    # count users with emails
    # remove unnecessary columns to prevent errors in uploads
    for csvfile in csvfiles:
        csv_path = os.path.join(target_path, csvfile)
        with open(csv_path, newline='', encoding='Windows-1252') as _csvfile:
            rows = csv.DictReader(_csvfile, delimiter=',', quotechar='"')
            for row in rows:
                total += 1
                contact = process_row_fn(row)
                if contact:
                    total_edm_contacts += 1
                    edm_contacts.append(contact)

    print('Processed "{}" and found {} users, {} with Emails! Writing to files...'.format(_csvfile.name, total, total_edm_contacts))

    for output_path in output_paths:
        # Write to combined file
        with open(output_path, 'a', newline='') as _csvfile:
            writer = csv.DictWriter(_csvfile, CSV_HEADERS)
            writer.writerows(edm_contacts)

    print('Appended to', output_paths, '\n')


def process_toreta_row(row):
    # check for users with email1
    if row['email1']:
        return {
            'firstname': row['first_name'],
            'lastname': row['last_name'],
            'email': row['email1'],
        }
    else:
        return None


def process_chope_row(row):
    # check for users with email1
    if row['Email Address']:
        return {
            'firstname': row['Diner Name'],
            'email': row['Email Address'],
        }
    else:
        return None


def process_camcard_row(row):
    # email may have multiple values
    email = None
    emails = re.findall("[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}", row['Email'])
    if emails:
        email = emails[0]

    # check for users with email1
    if email:
        return {
            'firstname': row['First Name'],
            'lastname': row['Last Name'],
            'email': email,
        }
    else:
        return None


def clear_upload_files():
    files = os.listdir(path=config.UPLOAD_FILES_DIR)
    for f in files:
        with open('{}/{}'.format(config.UPLOAD_FILES_DIR, f), 'w+', newline='') as _csvfile:
            writer = csv.DictWriter(_csvfile, CSV_HEADERS)
            writer.writeheader()

    print('Emptied these files:', files, '\n')
