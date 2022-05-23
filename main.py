import sys
import re
import xml.etree.ElementTree as et
import argparse

parser = argparse.ArgumentParser("Download all files from a podcast on archive.org")


def mainreal(args):
    rgx = re.compile("^https?")
    isfile = True if rgx.match(args[1]) is None else False
    
    treeroot = None
    if isfile:
        treeroot = openxmlfile(args[1])
    return 0

def main(args):
    if len(args) < 2:
        help()
        return 0
    file_or_link = args[-1]

def openxmlfile(filename):
    try:
        xmltree = None
        with open(filename) as doc:
            xmltree = et.parse
        return xmltree.getroot()
    except:
        pass

def help():
    print("Help")

def parsearg():
    return 0

class Audio:
    def init(self):
        return 0

if __name__ == "__main__":
    main(sys.argv)
