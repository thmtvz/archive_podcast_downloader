import sys
import re
import xml.etree.ElementTree as et
import argparse

parser = argparse.ArgumentParser("Download all files from a podcast on archive.org")


def mainreal(args):
    pass


def main(args):
    try:
        isfile, file_or_link = processargs(args)
    except Exception as Exc:
        help(True, Exc)

def openxmlfile(filename):
    xmltree = None
    with open(filename) as doc:
        xmltree = et.parse(doc)
    return xmltree.getroot()

def help(err, errmsg):
    if err:
        print("Error: ", errmsg)
    print("Help")

def parsearg():
    return 0

def processargs(args):
    if len(args) < 2:
        raise Exception("Not enouth arguments")
    rgx = re.compile("^https?")
    file_or_link = args[-1]
    isfile = True if rgx.match(file_or_link) is None else False

    return (isfile, file_or_link)

class Audio:
    def init(self):
        return 0

if __name__ == "__main__":
    main(sys.argv)
