from sanitize_and_convert import SanitizePepperData as Sanitizer
import requests
import pandas as pd
from datetime import datetime
import json
import urllib2
import re
from pprint import pprint as pp
import sys
import pdb
import os
from bs4 import BeautifulSoup


class FetchData():
    """Fetch and write peppers data either through static HTML or AJAX POST request"""
    def __init__(self, how="scrape", write=False, output_path=None):
        """Load data through scraper (how="scrape") or static parser (how="parse")"""
        if how == "scrape":
            self.source = PepperScraper()
        elif how == "parse":
            self.source = StaticPepperParser()

        self.raw_data = self.source.raw_data

        sanitizer = Sanitizer(self.source.labeled_data)
        self.data = sanitizer.clean
        self.json = self.data.to_dict(orient="records")

        if write:
            self.write_json(output_path)

    def write_json(self, output_path):
        header_info = """{
        "source": "https://www.pepperscale.com/hot-pepper-list/",
        "contact": "https://github.com/alemosie",
        "last_updated": "%s",
        "peppers":
        """ % (datetime.now())

        output_dir = "data" if not output_path else output_path
        json_file = "{}/peppers_{}.json".format(output_dir, str(datetime.now().date()).replace("-",""))
        print "Writing to %s..." % json_file
        with open (json_file, "w") as json_file:
            json_file.write(header_info)
            json_file.write(self.data.to_json(orient='records'))
            json_file.write("}")


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

class StaticPepperParser():
    """Parse data from static PepperScale.com HTML, procured on 11 Oct, 2017"""
    def __init__(self):
        self.raw_data = self.fetch_raw_pepper_html()
        self.labeled_data = [self.label_html_data(pepper_row) for pepper_row in self.raw_data]

    def fetch_raw_pepper_html(self):
        with open("data/static_pepperscale_data.html", "r") as raw_html:
            self.pepper_html = BeautifulSoup(raw_html, 'html.parser')

        raw_peppers = self.pepper_html.find_all("tr", re.compile("even|odd"))
        print "%d peppers fetched!" % len(raw_peppers)
        return raw_peppers

    def label_html_data(self, row_tag):
        labels = ["name", "min_shu", "max_shu", "heat", "jrp", "species", "origin", "link"]
        pepper_info = [element.text.encode("utf-8") for element in row_tag.contents if element.text != "pepperscale.com"]
        link = str(row_tag.find("a"))
        return dict(zip(labels, pepper_info + [link]))


if __name__ == '__main__':

    print "\nFetch data\n--------------------------------------------------\n"

    if len(sys.argv) == 1 or (len(sys.argv) == 2 and "-sc" in sys.argv):
        print "Launching AJAX request to PepperScale...\n"
        fetcher = FetchData()

    elif len(sys.argv) == 2 and "-st" in sys.argv:
        print "Parsing raw, static HTML from PepperScale website...\n"
        fetcher = FetchData(how="parse")

    elif len(sys.argv) > 1 and "-w" in sys.argv:
        path_arg = [arg for arg in sys.argv[1:] if os.path.isdir(arg)]
        output_path = path_arg[0] if len(path_arg) > 0 else None

        if "-st" in sys.argv:
            print "Parsing raw, static HTML from PepperScale website...\n"
            fetcher = FetchData(how="parse", write=True, output_path=output_path)
        else:
            print "Launching AJAX request to PepperScale...\n"
            fetcher = FetchData(write=True, output_path=output_path)

    print "\nResults (first 2 entries):\n"
    pp(fetcher.json[:2])