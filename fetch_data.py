import pepperscale_fetcher
import chiliworld_fetcher
import hotstuff_fetcher
import cayenne_diane_fetcher

from packages import *

### CONSTANTS

SCHEMA =  [
    "name", "species", "heat", "region", "origin", "min_shu", "max_shu",
    "min_jrp", "max_jrp", "link", "source_name"
]

HEADERS = {
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
}

DRIVER_PATH = '/Users/asiega/Development/chromedriver' # for selenium

### FETCHER

class Fetcher():
    """Fetch and contain pepper data from a variety of web sources"""
    def __init__(self):
        self.pepperscale = pepperscale_fetcher.run(HEADERS, SCHEMA)
        self.chiliworld = chiliworld_fetcher.run(HEADERS)
        self.hotstuff = hotstuff_fetcher.run(HEADERS, DRIVER_PATH)
        self.cayenne_diane = cayenne_diane_fetcher.run(HEADERS)
        self.all = pd.concat([self.pepperscale, self.chiliworld, self.hotstuff, self.cayenne_diane])
        print("\n🌶️  %d total peppers fetched 🌶️ " % len(self.all))


### WRITERS

def write_json(data, output_dir="data"):
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
        f.write(data[SCHEMA].to_json(orient='records'))
        f.write("}")

def write_csv(data, output_dir="data"):
    csv_file = "{}/peppers_{}.csv".format(output_dir, str(datetime.now().date()).replace("-",""))
    print("Writing to %s..." % csv_file)
    data[SCHEMA].to_csv(csv_file, index=False)

### RUNNER

if __name__ == '__main__':

    print("\nFetch data\n--------------------------------------------------\n")
    data = Fetcher()

    if len(sys.argv) > 1:
        path_arg = [arg for arg in sys.argv[1:] if os.path.isdir(arg)]
        output_dir = path_arg[0] if len(path_arg) > 0 else "data"

        if "-json" in sys.argv:
            write_json(data.all, output_dir)
        elif "-csv" in sys.argv:
            write_csv(data.all, output_dir)
        elif "-w" in sys.argv:
            write_json(data.all, output_dir)
            write_csv(data.all, output_dir)

    print("\nResults (first 3 entries):\n")
    pp(data.all[:3])
