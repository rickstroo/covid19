# import a commonly used command line argument parser
import argparse

# parse the command line
parser = argparse.ArgumentParser(description='Extracts measurements from DICOM SR as XML and outputs as JSON.')
parser.add_argument("-f", "--file", required=True, type=str, help="The name of the file to parse")
args = parser.parse_args()

# pick up the name of the dicom file from the command line
file = args.file

# import dicom library
# requires "pip3.8 install pydicom"
import pydicom

# read the dicom object
dataset = pydicom.dcmread('/Users/Rick/data/dicom/GENECG.dcm')
print(dataset)

# this is an example of how to extract a single element
acn = dataset[0x0008,0x0050]
print(acn)

# import an XML parser
# requires "pip3.8 install untangle"
import untangle

# define a resource using XML, just to figure out how to extract values
xml = '<organization><id>GRH</id><name>Grand River Hospital</name><address><country>Canada</country></address></organization>'
print(xml)

# extract some attributes, its very easy using untangle
doc = untangle.parse(xml)
id = doc.organization.id.cdata
print(id)
name = doc.organization.name.cdata
print(name)
country = doc.organization.address.country.cdata
print(country)

# import fhir resources
# requires "pip3.8 install fhir.resources"
from fhir.resources.organization import Organization
from fhir.resources.address import Address

# create a fhir resource the "python" way
org = Organization()
org.id = id
org.name = name
org.address = list()
addr = Address()
addr.country = country
org.address.append(addr)

# print the fhir resource as a JSON object
print(org.as_json())
