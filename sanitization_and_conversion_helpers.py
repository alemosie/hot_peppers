import pandas as pd
from datetime import datetime
import json

#### GENERAL FUNCTIONS

## Run all sanitization

def sanitize_pepper_data(data):
    data["min_shu"] = sanitize_shu(data, "min_shu")
    data["max_shu"] = sanitize_shu(data, "max_shu")
    data[["min_jrp", "max_jrp"]] = sanitize_jrp(data)
    data["heat"] = sanitize_heat(data)
    data["species"] = sanitize_species(data)
    data["origin"] = sanitize_field(data, "origin", sanitize_origin_value)
    data["region"] = sanitize_field(data, "origin", add_region_value)
    data["link"] = sanitize_link(data)
    return data
    
## General sanitization construct: clean value, clean series of values

def sanitize_field(data, field, value_sanitization_function):
    return data[field].apply(value_sanitization_function)

## JSON conversion

def to_json(sanitized_data, columns):
    json_data = sanitized_data[columns]
    
    header_info = """{
    "source": "https://www.pepperscale.com/hot-pepper-list/",
    "contact": "https://github.com/alemosie",
    "last_updated": "%s",
    "peppers":
    """ % (datetime.now())

    json_file = "data/peppers_{}.json".format(str(datetime.now().date()).replace("-",""))
    print "Writing to %s..." % json_file
    with open (json_file, "w") as json_file:
        json_file.write(header_info)
        json_file.write(json_data.to_json(orient='records'))
        json_file.write("}")
    
           
#### FIELD FUNCTIONS

## Link

def sanitize_link(data):
    return data["link"].apply(lambda x: x.split('"')[1])
    
## Min/max SHU

def sanitize_shu(data, shu_field):
    return data[shu_field].apply(lambda x: int(x) if x != "" else None)

## JRP -> min/max JRP

def sanitize_jrp_value(jrp):
    jrp = jrp.replace("equal", "0")

    if jrp == "0":
        return [0,0]
    elif "to" not in jrp:
        return [int(val.replace(",", "")) for val in jrp.split(" - ")]
    return [int(val.replace(",", "")) for val in jrp.split(" to ")]

def sanitize_jrp(data):
    """creates dataframe with min and max JRP columns from raw JRP range"""
    return pd.DataFrame(data["jrp"].apply(sanitize_jrp_value).values.tolist())


## Heat

def sanitize_heat(data):
    return data["heat"].apply(lambda x: x if x != "" else "Medium")


## Species

def sanitize_species(data):
    return data["species"].apply(lambda x: x if x != "N/A" else None)


## Origin

def sanitize_origin_value(origin):
    if pd.isnull(origin):
        return origin
    elif "Mexico" in origin and "South America" in origin:
        return "Mexico, South America"
    elif origin in ["USA", "United States"]:
        return "United States"
    elif origin not in ["N/A", "Unknown"]:
        return origin


## Region (new field to standardize origin)

def add_region_value(origin):
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