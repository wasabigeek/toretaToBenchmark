# FOR DOWNLOADING
TORETA_RAW_DATA_DIR = 'raw_data/toreta'
ARCHIVES_DIR = 'raw_data/archives'

TORETA_ACCOUNTS = [
    {
        'venue': 'venue2',
        'login_url': '',
        'download_url': '',
        'email': '',
        'password': '',
    },
    {
        'venue': 'venue1',
        'login_url': '',
        'download_url': '',
        'email': '',
        'password': '',
    }
]

# FOR FILE CLEANING
UPLOAD_FILES_DIR = 'UploadFiles'

benchmark1_venue1MarketingList = UPLOAD_FILES_DIR + ''
benchmark1_venue2MarketingList = UPLOAD_FILES_DIR + ''
benchmark2_venue2MailingList = UPLOAD_FILES_DIR + ''
benchmark2_venue2venue1MailingList = UPLOAD_FILES_DIR + ''
folder_mapping = [
    {
        "folder": "raw_data/toreta/venue2",
        "file_source": 'toreta',
        "output_paths": [
            benchmark1_venue2MarketingList,
            benchmark2_venue2MailingList,
            benchmark2_venue2venue1MailingList,
        ]
    },
    {
        "folder": "raw_data/toreta/venue1",
        "file_source": 'toreta',
        "output_paths": [
            benchmark1_venue1MarketingList,
            benchmark2_venue2venue1MailingList,
        ]
    },
    {
        "folder": "raw_data/camcard/venue2",
        "file_source": 'camcard',
        "output_paths": [
            benchmark1_venue2MarketingList,
            benchmark2_venue2venue1MailingList,
        ]
    },
]

# FOR UPLOADING
BENCHMARK_APIURL = 'http://api.benchmarkemail.com/1.3'
BENCHMARK = [
    {  # venue1
        'username': '',
        'password': '',
        'lists': [
            {
                'name': 'venue1 Marketing List',
                'id': '',
                'uploadfile': benchmark1_venue1MarketingList,
            },
            {
                'name': 'venue2 Marketing List',
                'id': '',
                'uploadfile': benchmark1_venue2MarketingList,
            },
        ],
    },
    {  # venue2
        'username': '',
        'password': '',
        'lists': [
            {
                'name': 'venue2 Mailing List',
                'id': '',
                'uploadfile': benchmark2_venue2MailingList,
            },
            {
                'name': 'venue2/venue1 Mailing List',
                'id': '',
                'uploadfile': benchmark2_venue2venue1MailingList,
            },
        ],
    },
]
