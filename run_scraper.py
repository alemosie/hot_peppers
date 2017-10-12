print "Importing packages..."

from sanitize_and_convert import SanitizePepperData as Sanitizer
import requests
import pandas as pd
from datetime import datetime
import json
import urllib2
import re
from pprint import pprint as pp
import sys


print "\nData Fetching\n--------------------------------------------------\n"

print "Launching AJAX request to PepperScale...\n"

# info from AJAX request made to "https://www.pepperscale.com/wp-admin/admin-ajax.php/"
# for <tbody> info on 'https://www.pepperscale.com/hot-pepper-list'

class PepperScraper():
    """Dynamically scrape hot pepper table data from PepperScale Hot Pepper List"""
    def __init__(self):
        self.headers = {
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        }
        self.base_url = "https://www.pepperscale.com/hot-pepper-list/"
        self.ajax_url = "https://www.pepperscale.com/wp-admin/admin-ajax.php/"
        self.raw_data = self.scrape_page()
        self.labeled_data = self.label_response_data(self.raw_data)
        print "%d peppers fetched!" % len(self.labeled_data)

    def fetch_nonces(self):
        """Nonces are dynamically generated on a regular (daily?) basis, and need to be scraped from the
        <script> tags at the time of the scraping request"""
        request = urllib2.Request(self.base_url, headers=self.headers)
        page_html = urllib2.urlopen(request).read()
        return re.findall('"nonce":"(\w+)"', page_html)

    def launch_ajax_request(self, nonce):
        """Submit a POST request to AJAX URL to get JS-generated table content"""
        request_fields = {
            "start": 0,
            "length": 10000,
            "action":"gv_datatables_data",
            "view_id": 10294,
            "nonce": nonce,
         }

        return requests.post(self.ajax_url, headers=self.headers,
                             data=request_fields, json={"key":"value"}).json()["data"]

    def scrape_page(self):
        """Try all nonces found on the page until the Golden Nonce is revealed!"""
        nonces = self.fetch_nonces()
        for nonce in nonces:
            try:
                return self.launch_ajax_request(nonce)
            except:
                pass

    def label_response_data(self, raw_data):
        labels = ["name", "link", "min_shu", "max_shu", "heat", "jrp", "species", "origin"]
        return [dict(zip(labels, entry)) for entry in raw_data]


pepper_scraper = PepperScraper()

print "Response: %d entries" % len(pepper_scraper.raw_data)
print "First two entries:"
pp(pepper_scraper.raw_data[:2], indent=4)


print "\n\nData Shaping & Sanitization\n--------------------------------------------------\n"

print "Labeling pepper entries..."

print "\nSanitizing data..."
sanitized = Sanitizer(pepper_scraper.labeled_data)

print "\nResult (first two entries):"
pp(sanitized.clean.iloc[:2], indent=4)

if len(sys.argv) > 1 and sys.argv[1] == "-w":
    print "\nJSON Conversion\n--------------------------------------------------\n"
    sanitized.write_json()

print "\nDone!\n"
