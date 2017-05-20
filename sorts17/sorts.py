import xml
from xml.sax import make_parser


class XMLReader(xml.sax.ContentHandler):
    def __init__(self, imported=False, mywin=None):
        xml.sax.ContentHandler.__init__(self)
        self.data = ""
        self.sortType = ""
        self.code = ""

    def characters(self, data):
        self.data += data

    def endElement(self, elem):
        elem = str(elem)
        if elem == "name":
            self.sortType = self.data
        elif elem == "code":
            self.code = self.data
        self.data = ""


parser = make_parser()
xml_reader = XMLReader()
parser.setContentHandler(xml_reader)
parser.parse("resources/quicksort.xml")

print xml_reader.sortType
exec xml_reader.code

print sort([1, 4, 7, 2, -1, 7])
