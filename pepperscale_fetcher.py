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

# set constants

HEADERS = {
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
}
BASE_URL = "https://www.pepperscale.com/hot-pepper-list/"
AJAX_URL = "https://www.pepperscale.com/wp-admin/admin-ajax.php/"

### FETCHER FUNCTIONS

def fetch_nonces():
    """Nonces are dynamically generated on a regular (daily?) basis, and need to be scraped from the
    <script> tags at the time of the scraping request"""
    # Python2
    # request = urllib2.Request(self.base_url, headers=self.headers)
    # page_html = urllib2.urlopen(request).read()

    request = urllib.request.Request(BASE_URL, headers=HEADERS)
    page_html = urllib.request.urlopen(request).read().decode('utf-8')
    return re.findall('"nonce":"(\w+)"', page_html)

def launch_ajax_request(nonce):
    """Submit a POST request to AJAX URL to get JS-generated table content"""
    request_fields = {
        "start": 0,
        "length": 10000,
        "action":"gv_datatables_data",
        "view_id": 10294,
        "nonce": nonce,
     }

    return requests.post(AJAX_URL, headers=HEADERS,
                         data=request_fields, json={"key":"value"}).json()["data"]

def scrape_page():
    """Try all nonces found on the page until the Golden Nonce is revealed!"""
    nonces = fetch_nonces()
    for nonce in nonces:
        try:
            return launch_ajax_request(nonce)
        except:
            pass

def label_response_data(raw_data):
    labels = ["name", "link", "min_shu", "max_shu", "heat", "jrp", "species", "origin"]
    return pd.DataFrame([dict(zip(labels, entry)) for entry in raw_data])

def run(schema):
    # scrape data
    raw_data = scrape_page()
    labeled_data = label_response_data(raw_data)
    print("%d peppers fetched!" % len(labeled_data))

    # sanitize data
    sanitized_data = sanitize(labeled_data, schema)
    return sanitized_data


### SANITIZATION FUNCTIONS

def sanitize(data, schema):
    """Run all PepperScale sanitization functions; produce clean copy of raw data"""
    data["min_shu"] = _sanitize_shu(data, "min_shu")
    data["max_shu"] = _sanitize_shu(data, "max_shu")
    data[["min_jrp", "max_jrp"]] = _sanitize_jrp(data)
    data["heat"] = _sanitize_heat(data)
    data["species"] = _sanitize_species(data)
    data["origin"] = _sanitize_field(data, "origin", _sanitize_origin_value)
    data["region"] = _sanitize_field(data, "origin", _add_region_value)
    data["link"] = _sanitize_link(data)
    data["source_name"] = "PepperScale"

    return data[schema]

### Field helper functions

def _sanitize_field(raw, field, value_sanitization_function):
    return raw[field].apply(value_sanitization_function)

def _sanitize_link(raw):
    return raw["link"].apply(lambda x: x.split('"')[1])

def _sanitize_shu(raw, shu_field):
    return raw[shu_field].apply(lambda x: int(x) if x != "" else None)

def _sanitize_jrp_value(jrp):
    jrp = jrp.replace("equal", "0")

    if jrp == "0":
        return [0,0]
    elif "to" not in jrp:
        return [int(val.replace(",", "")) for val in jrp.split(" - ")]
    return [int(val.replace(",", "")) for val in jrp.split(" to ")]

def _sanitize_jrp(raw):
    """creates dataframe with min and max JRP columns from raw JRP range"""
    return pd.DataFrame(raw["jrp"].apply(_sanitize_jrp_value).values.tolist())

def _sanitize_heat(raw):
    return raw["heat"].apply(lambda x: x if x != "" else "Medium").str.lower()

def _sanitize_species(raw):
    return raw["species"].apply(lambda x: x if x != "N/A" else None)

def _sanitize_origin_value(origin):
    if pd.isnull(origin):
        return origin
    elif "Mexico" in origin and "South America" in origin:
        return "Mexico, South America"
    elif origin in ["USA", "United States"]:
        return "United States"
    elif origin not in ["N/A", "Unknown"]:
        return origin

def _add_region_value(origin):
    """New field to standardize origin"""
    if origin in ["Italy", "United Kingdom", "Spain", "Hungary", "France"]:
        return "Europe"
    elif origin in ["USA", "United States", "Mexico"]:
        return "North America"
    elif origin in ["Trinidad", "Caribbean", "Jamaica",  "Panama", "Costa Rica"]:
        return "Central America and the Caribbean"
    elif origin in ["Peru", "Brazil", "Bolivia", "French Guyana", "South America"]:
        return "South America"
    elif origin in ["India", "Pakistan", "Thailand", "Japan", "China", "Phillipines"]:
        return "Asia"
    elif origin in ["Africa"]:
        return "Africa"
    elif origin in ["Australia"]:
        return "Australia and Oceania"
    elif origin in ["Syria"]:
        return "Middle East"
    elif pd.notnull(origin):
        return "Multi-Region"
