import os
import csv
import re
import datetime

current_directory = os.path.dirname(os.path.abspath(__file__))

today_str = datetime.datetime.now()
today_str = today_str.strftime('%d%b%Y')


def process_folder(input_folder, process_row_fn):

    target_path = os.path.join(current_directory, input_folder)

    print('\nSearching for CSV files in', target_path)
    csvfiles = [f for f in os.listdir(target_path) if f.endswith('.csv')]

    if not csvfiles:
        print("Couldn't find any CSV files :(\nMoving on...\n")
        return

    print('Found these CSV files: ', csvfiles)
    input_var = input('Do you want to process them? [y/n]: ')
    if input_var != 'y':
        print('OK, moving on!\n')
        return

    total = 0
    total_edm_contacts = 0
    edm_contacts = []

    # count users with emails
    # remove unnecessary columns to prevent errors in uploads
    for csvfile in csvfiles:
        csv_path = os.path.join(target_path, csvfile)
        with open(csv_path, newline='', encoding='Windows-1252') as _csvfile:
            print('Processing {0}'.format(_csvfile.name))

            rows = csv.DictReader(_csvfile, delimiter=',', quotechar='"')
            for row in rows:
                total += 1
                contact = process_row_fn(row)
                if contact:
                    total_edm_contacts += 1
                    edm_contacts.append(contact)

    # Write to combined file
    output_filename = 'combined_{0}_{1}.csv'.format(input_folder, today_str)
    output_path = os.path.join(current_directory, 'combined_breakdown', output_filename)
    with open(output_path, 'w', newline='') as _csvfile:
        fieldnames = ['first_name', 'last_name', 'phone1', 'email1']
        writer = csv.DictWriter(_csvfile, fieldnames)
        writer.writeheader()
        writer.writerows(edm_contacts)

    print('Processed {0} users, found {1} with Emails!'.format(total, total_edm_contacts))


def process_toreta_row(row):
    # check for users with email1
    if row['email1']:
        return {
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'phone1': row['phone1'],
            'email1': row['email1'],
        }
    else:
        return None


def process_chope_row(row):
    # check for users with email1
    if row['Email Address']:
        return {
            'first_name': row['Diner Name'],
            'phone1': row['Phone'],
            'email1': row['Email Address'],
        }
    else:
        return None


def process_camcard_row(row):
    # phone and email may have multiple values
    phone = None
    phones = re.findall("[\+]?[0-9]{1,16}", row['Phone'])
    if phones:
        phone = phones[0]

    email = None
    emails = re.findall("[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}", row['Email'])
    if emails:
        email = emails[0]

    # check for users with email1
    if email:
        return {
            'first_name': row['First Name'],
            'last_name': row['Last Name'],
            'phone1': phone,
            'email1': email,
        }
    else:
        return None


# MAGIC STARTS HERE
TORETA_FOLDER_NAMES = ['TABtoreta', 'LIBCtoreta']
CHOPE_FOLDER_NAMES = []
CAMCARD_FOLDER_NAMES = ['LIBCcamcard']

# TORETA
for folder in TORETA_FOLDER_NAMES:
    process_folder(input_folder=folder, process_row_fn=process_toreta_row)

# CHOPE
for folder in CHOPE_FOLDER_NAMES:
    process_folder(input_folder=folder, process_row_fn=process_chope_row)

# CAMCARD
for folder in CAMCARD_FOLDER_NAMES:
    process_folder(input_folder=folder, process_row_fn=process_camcard_row)
