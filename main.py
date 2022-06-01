import sys
import re
import time
import http.client
import urllib.parse
import xml.etree.ElementTree as et

READ = "r"
WRITE = "w"
BINARY_MODE = "b"
FILE_SUFFIX = ".mp3"
GET = "GET"


def main(args):
    try:
        name, dl = parsearg(args)
        rootnode = get_xml_root_node(name)
    except Exception as e:
        help(e)
        return
    
    il = make_items_list(rootnode)
    nd = []
    #todo finish this
    print("Starting downloads for %i items:" % (len(il)))
    ut = time.time()
    while len(il) != 0 and len(nd) == 0:
        item = il.pop()
        if item[1] > 3:
            continue
        try:
            download_file(item)
        except Exception as e:
            #todo add log for both stdout and file as an option
            nd.append((item[0], item[1] + 1))
            help(e)
        print("Done all in %d" % time.time() - ut)
    return

def download_file(item):
    item = item[0]
    fname = (item.title + FILE_SUFFIX).replace(" ", "_")
    print("\tDownloading %s as \"%s\"..." % (item.title, fname))
    t1 = time.time()
    data = makerequest(item.content)
    with open(fname, WRITE + BINARY_MODE) as f:
        print("\tWriting to file")
        f.write(data)
    t2 = time.time()
    print("\tDone in %d seconds" % (t2 - t1))
    return

def get_xml_root_node(name):
    rgx = re.compile("^https?")
    if rgx.match(name) is not None:
        d = makerequest(name)
        return et.fromstring(d)
    with open(name, "r") as f:
        return et.parse(f).getroot()

def help(err=""):
    if err != "":
        print("Error:", err, "\n")
    print("Usage: opd [OPTIONS] URL_OR_FILENAME")

def make_items_list(rootnode):
    itemslist = []
    channel = rootnode[0]
    for child in channel:
        if child.tag == "item":
            t = ""
            c = ""
            for i in child:
                if i.tag == "title":
                    t = i.text
                if i.tag == "enclosure":
                    c = i.attrib["url"]
            itemslist.append((PodcastItem(t, c), 0))
            
    return itemslist

def parsearg(args):
    file_or_link_name = args[-1]
    download_location = "."
    if len(args) < 2:
        raise Exception("Not enough arguments")
    if "--help" in args or "-h" in args:
        raise Exception("")
    if "--location" in args or "-l" in args:
        download_location = args

    return (file_or_link_name, download_location)

def makerequest(url):
    u = urllib.parse.urlparse(url)
    c = http.client.HTTPSConnection(u.hostname)
    
    c.request(GET, u.path + u.params + ("?" + u.query))
    res = c.getresponse()
    if res.status == 302:
        return makerequest(res.headers.get("Location"))
    data = res.read()
    return data

class PodcastItem:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        
if __name__ == "__main__":
    try:
        main(sys.argv)
    except BaseException:
        print("\nQuit")
