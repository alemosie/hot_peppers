print "Importing packages..."

from sanitize_and_convert import SanitizePepperData as Sanitizer
from bs4 import BeautifulSoup
import pdb
import pandas as pd
import re
from datetime import datetime
import json
from pprint import pprint as pp
import sys

print "\nData Fetching\n--------------------------------------------------\n"

print "Parsing raw, static HTML from PepperScale website..."
with open("data/static_pepperscale_data.html", "r") as raw_html:
    pepper_html = BeautifulSoup(raw_html, 'html.parser')


print "\nData Extraction\n--------------------------------------------------\n"

print "1) Verify that all 122 peppers in the PepperScale table are present in the base HTML extract"
# spot check of HTML -> all rows are "tr even" or "tr odd"
num_peppers = len(pepper_html.find_all("tr", re.compile("even|odd")))
print "\t", num_peppers == 122

print "\n2) Create pepper objects from HTML"
INFO_LABELS = ["name", "min_shu", "max_shu", "heat", "jrp", "species", "origin", "link"]
pepper_tags = pepper_html.find_all("tr", re.compile("even|odd"))

def extract_info_from_row_tag(row_tag):
    """Extract pepper info from tag; ignore non-pepper-related info"""
    pepper_info = [element.text.encode("utf-8") for element in row_tag.contents if element.text != "pepperscale.com"]
    link = str(row_tag.find("a"))
    return dict(zip(INFO_LABELS, pepper_info + [link]))

all_peppers = [extract_info_from_row_tag(pepper_row) for pepper_row in pepper_tags]
print "\tNumber of peppers: %d" % len(all_peppers)
print "\tFirst three peppers:"
pp(all_peppers[:3], indent=4)


print "\nData Sanitization\n--------------------------------------------------\n"

print "\nSanitizing data..."
sanitized = Sanitizer(all_peppers)
sanitized_pepper_data = sanitized.clean

print "\nResult (first two entries):"
pp(sanitized_pepper_data.iloc[:2], indent=4)


write = sys.argv[1].split("=")[1]
if write == "True":
    print "\nJSON Conversion\n--------------------------------------------------\n"

    sanitized.write_json()

    print "\nSample JSON objects:"
    pp(sanitized.json[:3], indent=4)


print "\n\nDone!\n"
