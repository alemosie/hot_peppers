import pepperscale_fetcher

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

SCHEMA =  [
    "name", "species", "heat", "region", "origin", "min_shu", "max_shu",
    "min_jrp", "max_jrp", "link", "source_name"
]

class Data():
    """Fetch and write peppers data from a variety of web sources"""
    def fetch(self):
        self.data = pepperscale_fetcher.run(SCHEMA)
        return self.data # with more fetchers, modify this to concat

    def write_json(self, output_dir="data"):
        header_info = """{
        "source": "https://www.pepperscale.com/hot-pepper-list/",
        "contact": "https://github.com/alemosie",
        "last_updated": "%s",
        "peppers":
        """ % (datetime.now())

        json_file = "{}/peppers_{}.json".format(output_dir, str(datetime.now().date()).replace("-",""))
        print("Writing to %s..." % json_file)
        with open (json_file, "w") as f:
            f.write(header_info)
            f.write(self.data.to_json(orient='records'))
            f.write("}")

    def write_csv(self, output_dir="data"):
        csv_file = "{}/peppers_{}.csv".format(output_dir, str(datetime.now().date()).replace("-",""))
        print("Writing to %s..." % csv_file)
        self.data.to_csv(csv_file, index=False)

if __name__ == '__main__':

    print("\nFetch data\n--------------------------------------------------\n")
    fetcher = Data()
    data = fetcher.fetch()

    if len(sys.argv) > 1:
        path_arg = [arg for arg in sys.argv[1:] if os.path.isdir(arg)]
        output_dir = path_arg[0] if len(path_arg) > 0 else "data"

        if "-json" in sys.argv:
            fetcher.write_json(output_dir)
        elif "-csv" in sys.argv:
            fetcher.write_csv(output_dir)

    print("\nResults (first 2 entries):\n")
    pp(data[:2])
