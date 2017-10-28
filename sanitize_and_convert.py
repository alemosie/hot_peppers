import pandas as pd
from datetime import datetime
import json

class SanitizePepperData():
    """From nested object containing raw, solely parsed pepper data,
    create a clean dataset for analysis"""
    def __init__(self, pepper_data, source_name):
        self.raw = pd.DataFrame(pepper_data)
        self.clean = self.sanitize_pepper_data(self.raw.copy(), source_name)

    #### GENERAL FUNCTIONS

    def sanitize_pepper_data(self, data, source_name):
        """Run all sanitization functions; produce clean copy of raw data"""
        data["min_shu"] = self.sanitize_shu("min_shu")
        data["max_shu"] = self.sanitize_shu("max_shu")
        data[["min_jrp", "max_jrp"]] = self.sanitize_jrp()
        data["heat"] = self.sanitize_heat()
        data["species"] = self.sanitize_species()
        data["origin"] = self.sanitize_field("origin", self.sanitize_origin_value)
        data["region"] = self.sanitize_field("origin", self.add_region_value)
        data["link"] = self.sanitize_link()
        data["source_name"] = source_name

        clean_cols = ["name", "species", "heat", "region", "origin", "min_shu", "max_shu", "min_jrp", "max_jrp", "link", "source_name"]
        return data[clean_cols]

    def sanitize_field(self, field, value_sanitization_function):
        return self.raw[field].apply(value_sanitization_function)

    #### FIELD FUNCTIONS

    ## Link

    def sanitize_link(self):
        return self.raw["link"].apply(lambda x: x.split('"')[1])

    ## Min/max SHU

    def sanitize_shu(self, shu_field):
        return self.raw[shu_field].apply(lambda x: int(x) if x != "" else None)

    ## JRP -> min/max JRP

    def sanitize_jrp_value(self, jrp):
        jrp = jrp.replace("equal", "0")

        if jrp == "0":
            return [0,0]
        elif "to" not in jrp:
            return [int(val.replace(",", "")) for val in jrp.split(" - ")]
        return [int(val.replace(",", "")) for val in jrp.split(" to ")]

    def sanitize_jrp(self):
        """creates dataframe with min and max JRP columns from raw JRP range"""
        return pd.DataFrame(self.raw["jrp"].apply(self.sanitize_jrp_value).values.tolist())

    ## Heat

    def sanitize_heat(self):
        return self.raw["heat"].apply(lambda x: x if x != "" else "Medium").str.lower()

    ## Species

    def sanitize_species(self):
        return self.raw["species"].apply(lambda x: x if x != "N/A" else None)

    ## Origin

    def sanitize_origin_value(self, origin):
        if pd.isnull(origin):
            return origin
        elif "Mexico" in origin and "South America" in origin:
            return "Mexico, South America"
        elif origin in ["USA", "United States"]:
            return "United States"
        elif origin not in ["N/A", "Unknown"]:
            return origin

    ## Region (new field to standardize origin)

    def add_region_value(self, origin):
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
