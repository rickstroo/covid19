import argparse

parser = argparse.ArgumentParser(description='Extracts measurements from DICOM SR as XML and outputs as JSON.')
parser.add_argument("-f", "--file", required=True, type=str, help="The name of the file to parse")
args = parser.parse_args()

file = args.file

# import dicom library
# requires "pip3.8 install pydicom"
import pydicom

dataset = pydicom.dcmread('/Users/Rick/data/dicom/GENECG.dcm')
print(dataset)
acn = dataset[0x0008,0x0050]
print(acn)

from xml.etree.ElementTree import fromstring as fs
import xmljson
from xmljson import badgerfish as bf
import json

xml = '<organization><id>GRH</id><name>Grand River Hospital</name><address><country>Canada</country></address></organization>'
print(xml)
obj = fs(xml)
print(obj)
print(json.dumps(bf.data(obj)))

# import fhir resources
# requires "pip3.8 install fhir.resources"
from fhir.resources.organization import Organization
from fhir.resources.address import Address

# create a fhir resource the "python" way
org = Organization()
org.id = "GRH"
org.name = "Grand River Hospital"
org.address = list()
addr = Address()
addr.country = "Canada"
org.address.append(addr)

# print the fhir resource as a JSON object
print(org.as_json())
