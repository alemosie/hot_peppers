print "Importing packages..."

from sanitization_and_conversion_helpers import * # sanitization & JSON conversion functions
import requests
import pandas as pd
from datetime import datetime
import json
from pprint import pprint as pp


print "\nData Fetching\n--------------------------------------------------\n"

print "Launching AJAX request to PepperScale...\n"

# info from AJAX request made for <tbody> info on 'https://www.pepperscale.com/hot-pepper-list'

headers = {
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}

request_fields = {
    "start":0,
    "length":10000, # max number of pepper entries to retrieve; currently 122, so we should be safe with 10k
    "action":"gv_datatables_data",
    "view_id": 10294,
    "nonce": "61b6a3f36a",
}
   
ajax_url = "https://www.pepperscale.com/wp-admin/admin-ajax.php/"

raw_pepper_data = requests.post(ajax_url, headers=headers, data=request_fields, json={"key":"value"}).json()["data"]

print "Response: %d entries" % len(raw_pepper_data)
print "First two entries:"
pp(raw_pepper_data[:2], indent=4)


print "\n\nData Shaping & Sanitization\n--------------------------------------------------\n"

print "Labeling pepper entries..."
INFO_LABELS = ["name", "link", "min_shu", "max_shu", "heat", "jrp", "species", "origin"]

def label_response_data(entry):
    labeled_entry = dict(zip(INFO_LABELS, entry))
    return labeled_entry

structured_pepper_data = [label_response_data(entry) for entry in raw_pepper_data]
pp(structured_pepper_data[:2], indent=4)

print "\nConverting to Pandas dataframe..."
pepper_data = pd.DataFrame(structured_pepper_data)

print "\nSanitizing data..."
sanitized_pepper_data = sanitize_pepper_data(pepper_data)

print "\nResult (first two entries):"
pp(sanitized_pepper_data.iloc[:2], indent=4)


print "\n\nJSON Conversion\n--------------------------------------------------\n"

JSON_COLS = ["name", "species", "heat", "region", "origin", "min_shu", "max_shu", "min_jrp", "max_jrp", "link"]
print "Subsetting data to:", JSON_COLS

to_json(sanitized_pepper_data, JSON_COLS)

print "\nDone!\n"