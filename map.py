# -*- coding: utf-8 -*-
"""

                        map.py
                        
                        
Script for visualizing where gopro photo locations on a map

"""

import os
import argparse
import gomap
import bokeh.plotting


def main(f, o):
    # find a list of folders
    folders = [d.strip() for d in f.split(",")]
    # get a list of all the image files in every folder
    print("Finding all the images...")
    imfiles = gomap.gather_images(f)
        
    # extract metadata
    print("Extracting metadata...")
    try:
        df = gomap.exif_df_mp(imfiles)
    except:
        df = gomap.exif_df(imfiles)
    print("%s images found"%len(df))
    # put the map together
    print("building map")
    p = gomap.generate_bokeh_map(df)
    bokeh.plotting.output_file(o)
    bokeh.plotting.show(p)
    print("done")





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize one or more directories of images")
    parser.add_argument("folder", type=str, help="top-level directory to search through for images")
    parser.add_argument("--outfile", type=str, help="output filename", default="gomap.html")
    args = parser.parse_args()
    
    main(args.folder, args.outfile)
