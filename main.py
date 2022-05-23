import sys
import re
import xml.etree.ElementTree as et

def mainreal(args):
    pass


def main(args):
    xml_dom_rootnode = None

    try:
        isfile, file_or_link = processargs(args)
    except Exception as err:
        help(True, err)
        return

    if isfile:
        try:
            xml_dom_rootnode = openxmlfile(file_or_link)
        except Exception as err:
            help(True, err)
            return
    return
                
        
def openxmlfile(filename):
    xmltree = None
    with open(filename, "r") as doc:
        try:
            xmltree = et.parse(doc)
        except Exception as e:
            raise e
        
    return xmltree.getroot()

def help(err, errmsg):
    if err:
        print("Error: ", errmsg)
    print("Help")

def parsearg():
    return

def processargs(args):
    if len(args) < 2:
        raise Exception("Not enouth arguments")
    rgx = re.compile("^https?")
    file_or_link = args[-1]
    isfile = True if rgx.match(file_or_link) is None else False

    return (isfile, file_or_link)

class PodcastItem:
    def init(self):
        return

if __name__ == "__main__":
    main(sys.argv)
