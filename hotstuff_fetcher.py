from bs4 import BeautifulSoup
import urllib
import pandas as pd
from selenium import webdriver
import pdb

BASE_URL = "http://ushotstuff.com/Heat.Scale.htm"
SEED_URL = "http://ushotstuff.com/"


### FETCHER FUNCTIONS

def run(headers, driver_path):
    # scrape and sanitize base pepper data
    base_html = _scrape_pepper_page(driver_path)
    base_data = [_extract_hotstuff_pepper_info(row) for row in base_html[1:] if _extract_hotstuff_pepper_info(row)] # skip colheader
    base_data = pd.DataFrame(base_data)
    base_data["source_name"] = "Uncle Steve's Hot Stuff"
    print("%d peppers fetched from HotStuff!" % len(base_data))

    # scrape seed data
    seed_html = _get_page_html("http://ushotstuff.com/", headers).find("table", class_="T1")
    seed_data = [_get_seed_row(row) for row in seed_html.find_all("tr")[1:]] # skip header row
    seed_data = pd.DataFrame(seed_data)

    # join seed data to base data, where available
    return base_data.merge(seed_data, how="left")

def _get_page_html(url, headers):
    request = urllib.request.Request(url, headers=headers)
    return BeautifulSoup(urllib.request.urlopen(request).read().decode('utf-8'), 'html.parser')

def _scrape_pepper_page(driver_path):
    # set up browser with selenium
    browser = webdriver.Chrome(executable_path=driver_path)
    browser.get(BASE_URL)

    # find and parse table element with all of the pepper rows
    table_xpath = '//*[@id="G2"]/tbody'
    table_element = browser.find_element_by_xpath(table_xpath)
    hotstuff_html = BeautifulSoup(table_element.get_attribute('innerHTML'), "html.parser")
    return hotstuff_html.find_all("tr")


## SANITIZATION FUNCTIONS

def _get_seed_row(row):
    row_tds = row.find_all("td")
    row_data = {
        "link": "http://ushotstuff.com/" + row.find("a")["href"],
        "heat": row_tds[1].text.lower(),
        "species": row_tds[2].text.lower()
    }
    return row_data

def _sanitize_shu(shu):
    shu = shu.text.strip().split(" ~ ")
    if len(shu) == 1:
        if "-" in shu[0]:
            min_shu, max_shu = shu[0].split("-")
            magnitude = "".join(max_shu.split(",")[1:])
            return [int(min_shu+magnitude), int(max_shu.replace(",", ""))]
        return [None, int(shu[0].replace(",", ""))]
    return [int(s.replace(",", "")) for s in shu]

def _sanitize_name(name):
    return name.text.strip()

def _get_link(link):
    if len(link.findChildren()) == 0:
        return BASE_URL # link, heat, species to match to seed data later
    return "http://ushotstuff.com/" + link.find("a", href=True)["href"] # only want first link

def _extract_hotstuff_pepper_info(row):
    elements = row.find_all("td")
    try:
        link, name, shu = [e for e in elements]
        name = _sanitize_name(name)
        link = _get_link(link)
        shu = _sanitize_shu(shu)
        return dict(zip(["name", "link", "min_shu", "max_shu"], [name, link] + shu))
    except: # malformed rows of not-quite-peppers at the end of the data; good for pepper comparison
        if len(row) > 1:
            name, shu = row.find_all('td')
            name = _sanitize_name(name)
            shu = _sanitize_shu(shu)
            link = "http://ushotstuff.com/Heat.Scale.htm"
            return dict(zip(["name", "link", "min_shu", "max_shu"], [name, link] + shu))
