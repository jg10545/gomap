import numpy as np
import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from dateutil.parser import parse

import multiprocessing as mp

def get_exif_data(image):
    """
    Returns a dictionary from EXIF data of a PIL image item
    """
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag,tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t,t)
                    gps_data[sub_decoded] = value[t]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
    return exif_data


def _convert_to_degrees(value):
    """
    Helper function to convert EXIF tags
    """
    if value is None:
        return None
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0)/float(d1)
    
    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0)/float(m1)
    
    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0)/float(s1)
    
    return d + (m/60) + (s/3600)

def retrieve_data(imfile):
    """
    Build a dictionary containing metadata for a single file.
    
    :imfile: string; path to the file
    """
    exif_data = get_exif_data(Image.open(imfile))
    outdict = {}
    
    if "GPSInfo" in exif_data:
        outdict["lon"] = _convert_to_degrees(exif_data["GPSInfo"].get("GPSLongitude", None))
        outdict["lon_ref"] = exif_data["GPSInfo"].get("GPSLongitudeRef", None)
        outdict["lat"] = _convert_to_degrees(exif_data["GPSInfo"].get("GPSLatitude", None))
        outdict["lat_ref"] = exif_data["GPSInfo"].get("GPSLatitudeRef", None)
        outdict["alt"] = exif_data["GPSInfo"].get("APSAltitude", None)
    outdict["timestamp"] = parse(exif_data["DateTime"])
    outdict["serial"] = exif_data.get("BodySerialNumber", None)
    outdict["file"] = imfile
    return outdict

def exif_df(filenames):
    """
    Load metadata for a list of file paths into a single
    pandas DataFrame
    """
    return pd.DataFrame([retrieve_data(f) for f in filenames])


def exif_df_mp(filenames):
    """
    Load metadata for a list of file paths into a single
    pandas DataFrame
    """
    pool = mp.Pool(processes=mp.cpu_count())
    #return pd.DataFrame([retrieve_data(f) for f in filenames])
    return pd.DataFrame(list(pool.map(retrieve_data, filenames)))