# Copyright (c) 2020 Rick Stroobosscher

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

# extract some values, its very easy using untangle
doc = untangle.parse(xml)
id = doc.organization.id.cdata
print(id)
name = doc.organization.name.cdata
print(name)
country = doc.organization.address.country.cdata
print(country)

# import fhir resources for organization
# requires "pip3.8 install fhir.resources"
from fhir.resources.organization import Organization
from fhir.resources.address import Address

# create a fhir organization the "python" way
org = Organization()
org.id = id
org.name = name
org.address = list()
address = Address()
address.country = country
org.address.append(address)

# print the fhir resource as a JSON object
print(org.as_json())

# import fhir resoures for observation
from fhir.resources.observation import Observation
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding

# create an observation
obs = Observation()
obs.id = '1' # should be generated
obs.status = 'final'
obs.category = list()
category = CodeableConcept()
category.coding = list()
code = Coding()
code.system = 'http://hl7.org/fhir/ValueSet/observation-category'
code.version = '4.0.1'
code.code = 'imaging'
code.display = 'imaging'
category.coding.append(code)
obs.category.append(category)
obs.code = CodeableConcept()
obs.code.coding = list()
code = Coding()
code.system = 'unknown'
code.version = 'unknown'
code.code = 'unknown'
code.display = 'pleural thickening'
obs.code.coding.append(code)

# more to do...

# print the observation as a JSON object
print(obs.as_json())
