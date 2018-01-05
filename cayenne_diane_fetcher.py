from packages import *

BASE_URL = "https://www.cayennediane.com/the-scoville-scale/"

### FETCHER FUNCTIONS

def run(headers, schema):
    cd_html = _get_page_html(BASE_URL, headers)
    cd_rows = cd_html.find("tbody").find_all("tr") # get table content rows without col headers
    print("%d peppers fetched from Cayenne Diane!" % len(cd_rows))

    return pd.DataFrame([_process_row(row, schema) for row in cd_rows])

def _get_page_html(url, headers):
    request = urllib.request.Request(url, headers=headers)
    return BeautifulSoup(urllib.request.urlopen(request).read().decode('utf-8'), 'html.parser')

def _process_row(row, schema):
    row_url = row.find("a")["href"] if row.find("a") else None
    row_data = [col.text for col in row.find_all("td")] + [row_url, BASE_URL] + ["Cayenne Diane"]
    row_data[1] = int(row_data[1].replace(",", ""))
    return dict(zip(schema, row_data))
