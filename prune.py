"""

                        prune.py
                        
                        
Script for pruning redundant images from one or more folders.

"""

import os
import argparse
import gomap


def main(f, t):
    # find a list of folders
    folders = [d.strip() for d in f.split(",")]
    # get a list of all the image files in every folder
    print("Finding all the images...")
    imfiles = []
    for f in folders:
        imfiles += [f + x for x in os.listdir(f) if "jpg" in x.lower()]
        
    # extract metadata
    print("Extracting metadata...")
    df = gomap.exif_df(imfiles)
    print("%s images found"%len(df))
    # find the images that are too close together
    close = gomap.find_close_images(df, t)
    print("Found %s images within %s meters of the previous one"%(len(close), t))
    
    print("\n")
    print("Do you want to delete these images? Seriously they'll be gone forever.")
    print("\n")
    inpt = input("(y/n) . ")
    if inpt.lower() == "y":
        print("Deleting...")
        for f in close["file"].values:
            os.system("rm %s"%f)
        print("Done")
    else:
        print("Then I guess we're done here")








if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prune one or more directories of images")
    parser.add_argument("folders", type=str, help="comma-delimited list of directories to check")
    parser.add_argument("--thresh", type=float, help="pruning distance (in radii)", default=2)
    args = parser.parse_args()
    
    main(args.folders, args.thresh)