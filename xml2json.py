import xmljson
from xml.etree.ElementTree import fromstring
from json import dumps
from xmljson import badgerfish

import argparse

parser = argparse.ArgumentParser(description='Extracts measurements from DICOM SR as XML and outputs as JSON.')
parser.add_argument("-f", "--file", required=True, type=str, help="The name of the file to parse")
args = parser.parse_args()

file = args.file

print(file)

str = '<employees><person><name value="Alice"/></person><person><name value="Bob"/></person></employees>'
print(str)
xml = badgerfish.data(fromstring(str))
json = dumps(xml)
print(json)
