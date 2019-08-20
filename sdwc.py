#!/usr/bin/env python

import json
import os
import requests
import sys
import wget
import argparse
import urllib.error

version = "v1.0.1"
verbose = False
baseURL = "https://www.reddit.com/"
sorting = "top"
subreddit = "earthporn"
orientation = "landscape"
imagesToGrab = 20
minResolution = {"height": 1080, "width": 1920}
outputDir = os.path.realpath(os.path.dirname(__file__)) + "/output"
parser = argparse.ArgumentParser(description="Crawl a subreddit for suitable wallpapers")

def main():
    if verbose:
        sys.stdout.write("subreddit........: " + subreddit + "\n")
        sys.stdout.write("sorting..........: " + sorting + "\n")
        sys.stdout.write("orientation......: " + orientation + "\n")
        sys.stdout.write("max images.......: " + str(imagesToGrab) + "\n")
        sys.stdout.write("min height.......: " + str(minResolution["height"]) + "\n")
        sys.stdout.write("min width........: " + str(minResolution["width"]) + "\n")
        sys.stdout.write("output directory.: " + outputDir + "\n")

    if not os.path.exists(outputDir):
        try:
            os.makedirs(outputDir)
        except OSError:
            sys.stdout.write("[  \033[0;31mERROR\033[m  ] Unable to create directory: " + outputDir + "\n")
    else:
        cleanOutputDirectory()

    grab();

    return

def grab(imagesGrabbed = 0, after = ""):
    response = requests.get(baseURL + subreddit + "/" + sorting + "/.json?limit=100" + after, headers = {"User-agent": "subreddit desktop wallpaper crawler " + version})
    jsondata = json.loads(response.text)

    if "error" in jsondata:
        sys.stdout.write("[  \033[0;31mERROR\033[m  ] " + jsondata["message"] + "\n")

    if "data" not in jsondata:
        sys.stdout.write("[  \033[0;31mERROR\033[m  ] Invalid data received: " + str(jsondata) + "\n")

        return

    if "children" not in jsondata["data"]:
        if verbose:
            sys.stdout.write("[ \033[0;33mWARNING\033[m ] No posts found on " + baseURL + subreddit + ".\n")

        return

    for item in jsondata["data"]["children"]:
        postURL = "Post"

        if imagesGrabbed == imagesToGrab:
            return

        if "data" not in item:
            if verbose:
                sys.stdout.write("[ \033[0;33mWARNING\033[m ] Subreddit contains no data.\n")

            continue

        if "id" in item["data"]:
            postURL = baseURL + subreddit + "/comments/" + item["data"]["id"]

        if "preview" not in item["data"]:
            if verbose:
                sys.stdout.write("[ \033[0;33mWARNING\033[m ] " + postURL + " contains no preview.\n")

            continue

        if "images" not in item["data"]["preview"]:
            if verbose:
                sys.stdout.write("[ \033[0;33mWARNING\033[m ] " + postURL + " contains no images.\n")

            continue

        for image in item["data"]["preview"]["images"]:
            if "source" not in image:
                if verbose:
                    sys.stdout.write("[ \033[0;33mWARNING\033[m ] " + postURL + " has no image source.\n")

                continue

            if "url" not in image["source"]:
                if verbose:
                    sys.stdout.write("[ \033[0;33mWARNING\033[m ] " + postURL + " has no image URL.\n")

                continue

            if "height" not in image["source"] or "width" not in image["source"]:
                if verbose:
                    sys.stdout.write("[ \033[0;33mWARNING\033[m ] " + postURL + " image does not have any dimension data.\n")

                continue

            if checkImageDimensions(image["source"]["height"], image["source"]["width"]):
                if downloadImage(image["source"]["url"]):
                    imagesGrabbed += 1
            else:
                if verbose:
                    sys.stdout.write("[ \033[0;33mWARNING\033[m ] " + postURL + " image does not meet dimension requirements.\n")
        pass
    pass

    if imagesGrabbed != imagesToGrab:
        if "after" not in jsondata["data"] or jsondata["data"]["after"] is None:
            if verbose:
                sys.stdout.write("[ \033[0;33mWARNING\033[m ] ")

            sys.stdout.write("Reached end of list after " + str(imagesGrabbed) + " of " + str(imagesToGrab) + " suitable wallpapers\n")
        else:
            grab(imagesGrabbed, "&after=" + jsondata["data"]["after"])

    return

def cleanOutputDirectory():
    for dirpath, dirnames, filenames in os.walk(outputDir):
        for name in filenames:
            path = os.path.join(dirpath, name)

            if path != outputDir + "/.gitkeep":
                os.unlink(path)

    return

def checkImageDimensions(height, width):
    if orientation == "landscape" and height > width:
        return False

    if orientation == "portrait" and height < width:
        return False

    if minResolution["height"] > height or minResolution["width"] > width:
        return False

    return True

def downloadImage(url):
    url = url.split("?")[0]
    fileName = url.split("/")[-1]

    if "preview.redd.it" in url:
        url = "https://i.redd.it/" + fileName

    try:
        wget.download(url, outputDir + "/" + fileName, wget.bar_thermometer)
        sys.stdout.write("\n")

        return True
    except urllib.error.HTTPError as httpError:
        sys.stdout.write("[  \033[0;31mERROR\033[m  ] Unable to download image from \"" + url + "\". " + str(httpError.code) + ": " + httpError.reason + "\n")
    except ValueError as valueError:
        sys.stdout.write("[  \033[0;31mERROR\033[m  ] " + str(valueError) + "\033[m\n")

    return False

parser.add_argument("-m", "--max",
    dest="imagesToGrab",
    metavar="",
    default=imagesToGrab,
    type=int,
    help="Number of images to download"
)

parser.add_argument("-o", "--orientation",
    dest="orientation",
    metavar="",
    default=orientation,
    type=str,
    help="Change orientation to user input [default: " + orientation + "]"
)

parser.add_argument("-r", "--subreddit",
    dest="subreddit",
    metavar="",
    default=subreddit,
    type=str,
    help="Change subreddit to user input [default: r/" + subreddit + "]"
)

parser.add_argument("-s", "--sorting",
    dest="sorting",
    metavar="",
    default=sorting,
    type=str,
    help="Change sorting to user input [default: " + sorting + "]"
)

parser.add_argument("-v", "--version",
    action="store_true",
    help="Show version information"
)

parser.add_argument("--min-width",
    dest="minWidth",
    metavar="",
    default=minResolution["width"],
    type=int,
    help="Change minimum resolution width constraint to user input [default: " + str(minResolution["width"]) + "]"
)

parser.add_argument("--min-height",
    dest="minHeight",
    metavar="",
    default=minResolution["height"],
    type=int,
    help="Change minimum resolution height constraint to user input [default: " + str(minResolution["height"]) + "]"
)

parser.add_argument("--output",
    dest="outputDir",
    metavar="",
    default=outputDir,
    type=str,
    help="Change output directory to user input [default: " + outputDir + "]"
)

parser.add_argument("--verbose",
    action="store_true",
    help="Print verbose process output"
)

args = parser.parse_args()

imagesToGrab = args.imagesToGrab
sorting = args.sorting
subreddit = "r/" + args.subreddit
orientation = args.orientation
minResolution["height"] = args.minHeight
minResolution["width"] = args.minWidth
outputDir = args.outputDir
verbose = args.verbose

if args.version:
    sys.stdout.write(os.path.basename(__file__) + " " + version + "\n")
    sys.exit(0)

main()
