import config
from utils.download import archive_old_csvs, login_and_download
from utils.clean import clear_upload_files, process_folder
from utils.upload import get_lists, list_is_correct, upload_file_to_benchmark

# DOWNLOAD TORETA -------------------------------------------------------------
input_var = input((
    'Do you want to archive old CSV files'
    ' and download the latest ones? [y/n]: '
))
if input_var == 'y':
    archive_old_csvs('raw_data/toreta')
    for account in config.toreta_accounts:
        login_and_download(account)
else:
    print('Moving on without archiving/downloading...\n')

# TO-DO: DOWNLOAD CAMCARD?
# TO-DO: DEDUPLICATE - for now, let Benchmark handle the deduplication

# EXTRACT AND CLEAN -----------------------------------------------------------
# Loop through Toreta / Camcard CSVs
# Pick out relevant columns from Toreta / Camcard
# Map data to Benchmark Lists
clear_upload_files()

for folder in config.folder_mapping:
    process_folder(
        input_folder=folder['folder'],
        file_source=folder['file_source'],
        output_paths=folder['output_paths'],
    )

# IMPORT TO BENCHMARK ---------------------------------------------------------
# Show lists before to check values
# Push cleaned data to Benchmark API

for benchmark in config.BENCHMARK:
    print('Retrieving lists for', benchmark['username'])
    retrieved_lists = get_lists(
        username=benchmark['username'],
        password=benchmark['password'],
    )

    for list_ in benchmark['lists']:
        if list_is_correct(current_list=list_, retrieved_lists=retrieved_lists):
            upload_file_to_benchmark(
                filepath=list_['uploadfile'],
                listname=list_['name'],
                listid=list_['id'],
                username=benchmark['username'],
                password=benchmark['password'],
            )
        else:
            print(
                "Couldn't find list ID:", list_['id'], "| Name:", list_['name'], "Stopping...")
            break

    get_lists(
        username=benchmark['username'],
        password=benchmark['password'],
        print_lists=True,
    )
    print('\n')
