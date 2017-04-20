# BENCHMARK CONTACT LIST UPDATER
Pulls down contacts from Toreta (http://toreta.in/), cleans the data and then uploads it to the respective Benchmark Email contact lists.

It can also clean data from CAMCARD, but you'll have to manually add it as a CSV to the respective folder.

## GETTING STARTED
- Tested with Python 3.5
- `pip install -r requirements.txt`
- Create a `config.py` file with login details and folder mappings (see `example-config.py`)
- Create the folder structure
- `cd` to the main directory and run `python update_edm_database.py`

P.S. there is plenty of mess!
