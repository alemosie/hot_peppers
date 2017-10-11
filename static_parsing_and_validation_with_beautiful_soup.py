from bs4 import BeautifulSoup
import pdb
import pandas as pd
import re
from datetime import datetime
import json
from pprint import pprint

print "\nParsing raw HTML from PepperScale website..."

with open("data/pepperscale_data.html", "r") as raw_html:
    pepper_html = BeautifulSoup(raw_html, 'html.parser')

print "Done\n"


print "\nData Extraction\n--------------------------------------------------\n"


print "1) Verify that all 122 peppers in the PepperScale table are present in the base HTML extract"

# spot check of HTML -> all rows are "tr even" or "tr odd"
num_peppers = len(pepper_html.find_all("tr", re.compile("even|odd")))

print "\t", num_peppers == 122



print "\n2) Create pepper objects from HTML"

INFO_LABELS = ["name", "min_shu", "max_shu", "heat", "jrp", "species", "origin", "link"]
pepper_tags = pepper_html.find_all("tr", re.compile("even|odd"))

def extract_info_from_row_tag(row_tag):
    """Extract pepper info from tag; ignore non-pepper-related info"""
    pepper_info = [element.text.encode("utf-8") for element in row_tag.contents if element.text != "pepperscale.com"]
    link = row_tag.find("a").get('href')
    return dict(zip(INFO_LABELS, pepper_info + [link]))

all_peppers = [extract_info_from_row_tag(pepper_row) for pepper_row in pepper_tags]
print "\tNumber of peppers: %d" % len(all_peppers)
print "\tFirst three peppers:"
pprint(all_peppers[:3], indent=4)


print "\n\nData Validation & Sanitization\n--------------------------------------------------\n"

peppers_data = pd.DataFrame(all_peppers)[INFO_LABELS]

## NAME

print "1) All names are unique, can be used as a unique ID"
print "\t Null values:",  peppers_data["name"].isnull().sum()
print "\t Unique: ", peppers_data["name"].nunique() == len(peppers_data)


## MIN/MAX SHU

print "\n\n2) Scoville heat units (SHU) are positive numbers (int/float)"

def validate_raw_shu(field):
    print "\t  Is null:", (~peppers_data[field].str.isdigit()).sum()
    print "\t  Type:", peppers_data[field].dtype
    print "\t  Min value:", repr(peppers_data[peppers_data[field].str.isdigit()][field].min())

print "\tMin SHU"
validate_raw_shu("min_shu")

print "\tMax SHU"
validate_raw_shu("max_shu")

print "\n\tSanitizing SHU fields..."

peppers_data["min_shu"] = peppers_data["min_shu"].apply(lambda x: int(x) if x != "" else None)
peppers_data["max_shu"] = peppers_data["max_shu"].apply(lambda x: int(x) if x != "" else None)

def validate_sanitized_shu(field):
    print "\t  Is null:", peppers_data[field].isnull().sum()
    print "\t  Type:", peppers_data[field].dtype
    print "\t  Min value:", repr(peppers_data[peppers_data[field].notnull()][field].min())

print "\tMin SHU"
validate_sanitized_shu("min_shu")

print "\tMax SHU"
validate_sanitized_shu("max_shu")


## JRP (Jalapeno reference point)

print "\n\n3) JRP range values are represented as 'min_jrp' and 'max_jrp'. JRP value is either a positive or negative number (int/float)."

def validate_jrp(field):
    print "\t  Is null:", peppers_data[field].isnull().sum()
    print "\t  Type:", peppers_data[field].dtype
    print "\t  Min value:", repr(peppers_data[field].min())
    print "\t  Malformed range:", (~peppers_data["jrp"].str.contains("to")).sum()

validate_jrp("jrp")

print "\n\tSanitizing JRP field..."

def sanitize_jrp(jrp):
    jrp = jrp.replace("equal", "0")

    if jrp == "0":
        return [0,0]
    elif "to" not in jrp:
        return [int(val.replace(",", "")) for val in jrp.split(" - ")]
    return [int(val.replace(",", "")) for val in jrp.split(" to ")]

peppers_data[["min_jrp", "max_jrp"]] = pd.DataFrame(peppers_data["jrp"].apply(sanitize_jrp).values.tolist())
validate_jrp("min_jrp")
print "\t  Example rows:"
pprint(peppers_data[["jrp", "min_jrp", "max_jrp"]].sample(3).to_dict(orient="records"), indent=6)


## HEAT

print "\n\n4) Heat values fall into PepperScale heat categories: 'Mild', 'Medium', 'Extra Hot', 'Super Hot'\n"

pprint(peppers_data["heat"].value_counts(dropna=False), indent=4)
print "\n\tSanitize malformed heat record..."
malformed_heat_record = peppers_data[peppers_data["heat"] == ""]
missing_heat = peppers_data[(peppers_data["heat"] != "") &
                            (peppers_data["min_shu"] >= malformed_heat_record["min_shu"].values[0]) &
                            (peppers_data["max_shu"] <= malformed_heat_record["max_shu"].values[0])]["heat"].unique()
print "\t  Missing heat category:", missing_heat
peppers_data["heat"] = peppers_data["heat"].apply(lambda x: x if x != "" else "Medium")
print "\t  All heat values after sanitization:", peppers_data["heat"].unique()


## SPECIES

print "\n\n5) Species values are all strings and valid species names. (Nulls should be NaN.)\n"

pprint(peppers_data["species"].value_counts(dropna=False))
print "\n\tSanitize N/As..."
peppers_data["species"] = peppers_data["species"].apply(lambda x: x if x != "N/A" else None)
print "\t  All species values after sanitization:", peppers_data["species"].unique()


## ORIGIN

print "\n\n6) Origin values are valid strings representing countries, regions, or continents. (Nulls, unknowns should be NaN.)\n"

print "\tAll origin values:"
pprint(peppers_data["origin"].sort_values().unique(), indent=6)

print "\tSanitizing origin field..."
def sanitize_origin(origin):
    if pd.isnull(origin):
        return origin
    elif "Mexico" in origin and "South America" in origin:
        return "Mexico, South America"
    elif origin in ["USA", "United States"]:
        return "United States"
    elif origin not in ["N/A", "Unknown"]:
        return origin

peppers_data["origin"] = peppers_data["origin"].apply(sanitize_origin)
print "\n\tAll origin values after sanitization:"
pprint(peppers_data["origin"].sort_values().unique(), indent=6)


print "\n\n7) New region field should represent a standardized origin: a region of the world. (Nulls, unknowns should be NaN.)\n"

def add_region(origin):
    if origin in ["Italy", "United Kingdom", "Spain", "Hungary", "France"]:
        return "Europe"
    elif origin in ["United States", "Mexico"]:
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

peppers_data["region"] = peppers_data["origin"].apply(add_region)
print "\tSample region values:"
pprint(peppers_data[["origin", "region"]].drop_duplicates().sample(3).to_dict(orient="records"), indent=4)


print "\nJSON Conversion\n--------------------------------------------------\n"


JSON_COLS = ["name", "species", "heat", "region", "origin", "min_shu", "max_shu", "min_jrp", "max_jrp", "link"]
json_peppers_data = peppers_data[JSON_COLS]

print "\tSample JSON objects:"
pprint(json_peppers_data.sample(3).to_json(orient='records'), indent=4)

print "\n"
