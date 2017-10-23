from sanitize_and_convert import SanitizePepperData as Sanitizer
import requests
import pandas as pd
from datetime import datetime
import json
import urllib.request # in Python2, it's urllib2
import re
from pprint import pprint as pp
import sys
import pdb
import os
from bs4 import BeautifulSoup


class FetchData():
    """Fetch and write peppers data either through static HTML or AJAX POST request"""
    def __init__(self, output_path=None):
        self.raw_data = self.source.raw_data
        self.output_path = output_path

    def sanitize_source_data(self, source):
        sanitizer = Sanitizer(source.labeled_data)
        self.data = sanitizer.clean
        self.json = self.data.to_dict(orient="records")

    def run_scraper(self):
        """Grab data through live AJAX request"""
        scraper = PepperScraper()
        self.source = scraper.run()
        self.sanitize_source_data(self.source)

    def run_parser(self):
        """Parse data from static PepperScale HTML"""
        parser = StaticPepperParser()
        self.source = parser.run()
        self.sanitize_source_data(self.source)

    def write_json(self):
        header_info = """{
        "source": "https://www.pepperscale.com/hot-pepper-list/",
        "contact": "https://github.com/alemosie",
        "last_updated": "%s",
        "peppers":
        """ % (datetime.now())

        output_dir = "data" if not self.output_path else self.output_path
        json_file = "{}/peppers_{}.json".format(output_dir, str(datetime.now().date()).replace("-",""))
        print("Writing to %s..." % json_file)
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

    def fetch_nonces(self):
        """Nonces are dynamically generated on a regular (daily?) basis, and need to be scraped from the
        <script> tags at the time of the scraping request"""
        # Python2
        # request = urllib2.Request(self.base_url, headers=self.headers)
        # page_html = urllib2.urlopen(request).read()

        request = urllib.request.Request(self.base_url, headers=self.headers)
        page_html = urllib.request.urlopen(request).read().decode('utf-8')
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

    def run(self):
        self.raw_data = self.scrape_page()
        self.labeled_data = self.label_response_data(self.raw_data)
        print("%d peppers fetched!" % len(self.labeled_data))


class StaticPepperParser():
    """Parse data from static PepperScale.com HTML, procured on 11 Oct, 2017"""
    def __init__(self, html_path="data/static_pepperscale_data.html"):
        self.html_path = html_path

    def fetch_raw_pepper_html(self):
        with open(self.html_path, "r") as raw_html:
            self.pepper_html = BeautifulSoup(raw_html, 'html.parser')

        raw_peppers = self.pepper_html.find_all("tr", re.compile("even|odd"))
        print("%d peppers fetched!" % len(self.labeled_data))
        return raw_peppers

    def label_html_data(self, row_tag):
        labels = ["name", "min_shu", "max_shu", "heat", "jrp", "species", "origin", "link"]
        pepper_info = [element.text.encode("utf-8") for element in row_tag.contents if element.text != "pepperscale.com"]
        link = str(row_tag.find("a"))
        return dict(zip(labels, pepper_info + [link]))

    def run(self):
        self.raw_data = self.fetch_raw_pepper_html()
        self.labeled_data = [self.label_html_data(pepper_row) for pepper_row in self.raw_data]
        print("%d peppers parsed!" % len(self.labeled_data))


if __name__ == '__main__':

    print("\nFetch data\n--------------------------------------------------\n")

    if len(sys.argv) == 1 or (len(sys.argv) == 2 and "-sc" in sys.argv):
        print("Launching AJAX request to PepperScale...\n")
        fetcher = FetchData()
        fetcher.run_scraper()

    elif len(sys.argv) == 2 and "-st" in sys.argv:
        print("Parsing raw, static HTML from PepperScale website...\n")
        fetcher = FetchData()
        fetcher.run_parser()

    elif len(sys.argv) > 1 and "-w" in sys.argv:
        path_arg = [arg for arg in sys.argv[1:] if os.path.isdir(arg)]
        output_path = path_arg[0] if len(path_arg) > 0 else None
        fetcher = FetchData(output_path=output_path)

        if "-st" in sys.argv:
            print("Parsing raw, static HTML from PepperScale website and writing output...\n")
            fetcher.run_parser()
            fetcher.write_json()
        else:
            print("Launching AJAX request to PepperScale and writing output...\n")
            fetcher.run_scraper()
            fetcher.write_json()

    print("\nResults (first 2 entries):\n")
    pp(fetcher.json[:2])
