# -*- coding: utf-8 -*-
import pandas as pd
import bokeh.plotting, bokeh.tile_providers
import pyproj





def generate_bokeh_map(df, tile=bokeh.tile_providers.CARTODBPOSITRON):
    """
    Generate a bokeh figure object that maps out the locations of
    your images
    
    :df: pandas DataFrame of EXIF metadata
    :tile: reference to tile server for the map
    """
    df = df.copy()
    # map any western-hemisphere longitudes to negative. latitude
    # version implemented the same but not tested
    df.loc[df["lon_ref"] == "W", "lon"] *= -1
    df.loc[df["lat_ref"] == "S", "lat"] *= -1
    
    # project lat-longs to webmercator, discarding nulls
    proj = pyproj.Proj(init="epsg:3857")
    x, y = proj(df.lon.values[pd.notnull(df.lon.values)], 
                df.lat.values[pd.notnull(df.lon.values)])
    
    # build bokeh figure object
    p = bokeh.plotting.figure(x_range=(x.min(), x.max()),
                         y_range=(y.min(), y.max()),
                          x_axis_type="mercator", y_axis_type="mercator")
    p.add_tile(tile)
    p.circle(x=x, y=y, alpha=0.25)
    return p