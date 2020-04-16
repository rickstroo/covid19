import argparse

parser = argparse.ArgumentParser(description='Extracts measurements from DICOM SR as XML and outputs as JSON.')
parser.add_argument("-f", "--file", required=True, type=str, help="The name of the file to parse")
args = parser.parse_args()

file = args.file

import pydicom

dataset = pydicom.dcmread('/Users/Rick/data/dicom/GENECG.dcm')
print(dataset)
acn = dataset[0x0008,0x0050]
print(acn)

from xml.etree.ElementTree import fromstring as fs
import xmljson
from xmljson import badgerfish as bf
import json

xml = '<employees><person><name value="Alice"/></person><person><name value="Bob"/></person></employees>'
print(xml)
print(json.dumps(bf.data(fs(xml))))
