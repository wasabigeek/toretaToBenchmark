import csv

from tabulate import tabulate

import config
from utils.bme_xmlrpc_python.BMEApi import BMEApi


def get_lists(username, password, print_lists=False):
    client = BMEApi(username, password, config.BENCHMARK_APIURL)
    if not client.isLogin:
        # an error occurred while logging in
        print("A fault occurred")
        print("Fault code: ", client.faultCode)
        print("Fault string: ", client.faultString)
        return

    result = client.listGet("", 1, 3, "", "")

    if not client.isOk:
        print("A fault occurred")
        print("Fault code: ", client.faultCode)
        print("Fault string: ", client.faultString)
        return

    if print_lists:
        table = []
        table.append(['ID', 'NAME', 'CONTACT COUNT', 'MODIFIED DATE'])
        for index, item in enumerate(result):
            table.append([
                result[index]['id'],
                result[index]['listname'],
                result[index]['contactcount'],
                result[index]['modifiedDate'],
            ])
        print(tabulate(table))

    return result


def list_is_correct(current_list, retrieved_lists):
    list_is_correct = False
    for retrieved_list in retrieved_lists:
        if (retrieved_list['id'] == current_list['id']) and (retrieved_list['listname'] == current_list['name']):
            print(
                'List match! ID:',
                retrieved_list['id'],
                '| Name:', retrieved_list['listname'],
                '| Contact Count:', retrieved_list['contactcount']
            )
            list_is_correct = True

    return list_is_correct


def upload_file_to_benchmark(filepath, listname, listid, username, password):
    client = BMEApi(username, password, config.BENCHMARK_APIURL)
    if not client.isLogin:
        # an error occurred while logging in
        print("A fault occurred")
        print("Fault code: ", client.faultCode)
        print("Fault string: ", client.faultString)
        return

    with open(filepath, newline='', encoding='Windows-1252') as _csvfile:
        contacts = list(csv.DictReader(_csvfile, delimiter=',', quotechar='"'))

    print(
        'Sending {contacts} contacts from "{uploadfile}" to "{listname}" (ID: {listid})...'.format(
            contacts=len(contacts),
            uploadfile=filepath,
            listname=listname,
            listid=listid,
        )
    )

    client.listAddContacts(listid, contacts)

    if not client.isOk:
        print("A fault occurred")
        print("Fault code: ", client.faultCode)
        print("Fault string: ", client.faultString)
        return
