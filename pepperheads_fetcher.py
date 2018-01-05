from packages import *

BASE_URL = "https://pepperheadsforlife.com/the-scoville-scale/"

def run(headers):
    ph_html = _get_page_html(BASE_URL, headers)
    ph_rows = ph_html.find("tbody").find_all("tr") # get table content rows without col headers
    print("%d peppers fetched from Pepperheads!" % len(ph_rows))

    return pd.DataFrame([_process_row(row) for row in ph_rows])

def _get_page_html(url, headers):
    request = urllib.request.Request(url,
                                     headers=headers)
    context = ssl._create_unverified_context()
    return BeautifulSoup(urllib.request.urlopen(request, context=context).read().decode('utf-8'), 'html.parser')

def _process_row(row):
    row_url = BASE_URL if not row.find("a") else row.find("a")["href"]
    row_data = [col.text for col in row.find_all("td")] + [row_url] + ["Pepperheads"]
    row_data[1] = int(row_data[1].replace(",", ""))
    return dict(zip(["name", "max_shu", "link", "source_name"], row_data))
