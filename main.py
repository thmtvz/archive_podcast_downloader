import sys
import re
import xml.etree.ElementTree as et
import http.client
import urllib.parse

def main(args):
    if len(args) < 2:
        help("Not enough arguments")
        return
    if "--help" in args or "-h" in args:
        help()
        return
    try:
        rootnode = get_xml_root_node(args[-1])
    except Exception as e:
        help(e)
        return
    
    
    il = make_items_list(rootnode)

    #todo finish this
    return

def get_xml_root_node(name):
    rgx = re.compile("^https?")
    if rgx.match(name) is not None:
        d = makerequest(name)
        return et.fromstring(d)
    with open(name, "r") as f:
        return et.parse(f).getroot()

def help(err=""):
    print("Usage: opd [OPTIONS] URL_OR_FILENAME")
    if err != "":
        print("\nError:", err)

def make_items_list(rootnode):
    itemslist = []
    channel = None
    for c in rootnode:
        channel = c
    #welp...
    for child in channel:
        if child.tag == "item":
            t = ""
            c = ""
            for i in child:
                if i.tag == "title":
                    t = i.text
                if i.tag == "enclosure":
                    c = i.attrib["url"]
            itemslist.append(PodcastItem(t, c))
            
    return itemslist

def makerequest(url):
    u = urllib.parse.urlparse(url)
    c = http.client.HTTPSConnection(u.hostname)
    link = u.path + u.params + ("?" + u.query)
    c.request("GET", link)
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
    main(sys.argv)
