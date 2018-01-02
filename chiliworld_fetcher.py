from packages import *

# set constants
BASE_URL = "https://www.chilliworld.com/factfile/scoville-scale#ChilliPepperScovilleScale"

### FETCHER FUNCTIONS

def run(headers):
    pepper_data = _scrape_page(headers)
    print("%d peppers fetched from ChiliWorld!" % len(pepper_data))

    peppers = [_sanitize_row(row) for row in pepper_data[1:]] # first row is header row
    return pd.DataFrame(peppers)

def _scrape_page(headers):
    request = urllib.request.Request(BASE_URL, headers=headers)
    raw_html = urllib.request.urlopen(request).read().decode('utf-8')
    page_html = BeautifulSoup(raw_html, 'html.parser')
    pepper_data = page_html.find(id="ChilliPepperScovilleScale").find_all("tr")
    return pepper_data


### SANITIZATION FUNCTIONS

def _sanitize_row(row):
    raw_shu, raw_name = [element.contents[0] for element in row.find_all("td")]
    name = _sanitize_name(raw_name)
    if name:
        sanitized_row = {}
        sanitized_row["name"] = name + " Pepper"
        sanitized_row["origin"] = _sanitize_location(raw_name)
        sanitized_row["min_shu"], sanitized_row["max_shu"] = _sanitize_shu(raw_shu)
        sanitized_row["source_name"] = "ChiliWorld"
        sanitized_row["link"] = BASE_URL
        return sanitized_row

def _sanitize_name(name):
    if "<b>" not in str(name):
        pepper_name = name.split("(")[0].split(",")[0]
        sanitized_pepper_name = pepper_name.lower().replace(" pepper", "").replace("the ", "")
        return " ".join([part.strip().capitalize() for part in sanitized_pepper_name.split()])

def _sanitize_shu(shu):
    shu = [int(val) for val in shu.replace(" (reported) ", "").replace(",", "").split(" - ")]
    if len(shu) == 1:
        return [None, shu[0]]
    return shu

def _sanitize_location(name):
    if name and "<b>" not in str(name):
        location = name.split("(")[1] if len(name.split("(")) > 1 else None
        if location and ("Wales" in location or "England" in location):
            return "United Kingdom"
        elif location and "South Carolina" in location:
            return "United States"
        elif location and "Australia" in location:
            return "Australia"
        return None
