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
from fhir.resources.fhirreference import FHIRReference
from fhir.resources.identifier import Identifier

# create an observation using json

json = {
  "resourceType": "Observation",
  "id": "blood-pressure",
  "meta": {
    "lastUpdated": "2014-01-30T22:35:23+11:00"
  },
  "text": {
    "status": "generated",
    "div": "<div><p><b>Generated Narrative with Details</b></p><p><b>id</b>: blood-pressure</p><p><b>meta</b>: </p><p><b>identifier</b>: urn:uuid:187e0c12-8dd2-67e2-99b2-bf273c878281</p><p><b>status</b>: final</p><p><b>code</b>: Blood pressure systolic &amp; diastolic <span>(Details : {LOINC code '55284-4' = 'Blood pressure systolic and diastolic', given as 'Blood pressure systolic &amp; diastolic'})</span></p><p><b>subject</b>: <a>Patient/example</a></p><p><b>effective</b>: 17/09/2012</p><p><b>performer</b>: <a>Practitioner/example</a></p><p><b>interpretation</b>: low <span>(Details : {http://hl7.org/fhir/v2/0078 code 'L' = 'Low', given as 'Below low normal'})</span></p><p><b>bodySite</b>: Right arm <span>(Details : {SNOMED CT code '368209003' = '368209003', given as 'Right arm'})</span></p><blockquote><p><b>component</b></p><p><b>code</b>: Systolic blood pressure <span>(Details : {LOINC code '8480-6' = 'Systolic blood pressure', given as 'Systolic blood pressure'}; {SNOMED CT code '271649006' = '271649006', given as 'Systolic blood pressure'}; {http://acme.org/devices/clinical-codes code 'bp-s' = '??', given as 'Systolic Blood pressure'})</span></p><p><b>value</b>: 107 mm[Hg]</p></blockquote><blockquote><p><b>component</b></p><p><b>code</b>: Diastolic blood pressure <span>(Details : {LOINC code '8462-4' = 'Diastolic blood pressure', given as 'Diastolic blood pressure'})</span></p><p><b>value</b>: 60 mm[Hg]</p></blockquote></div>"
  },
  "identifier": [
    {
      "system": "urn:ietf:rfc:3986",
      "value": "urn:uuid:187e0c12-8dd2-67e2-99b2-bf273c878281"
    }
  ],
  "status": "final",
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "55284-4",
        "display": "Blood pressure systolic & diastolic"
      }
    ]
  },
  "subject": {
    "reference": "Patient/example"
  },
  "effectiveDateTime": "2012-09-17",
  "performer": [
    {
      "reference": "Practitioner/example"
    }
  ],
  "interpretation": [
    {
        "coding": [
        {
            "system": "http://hl7.org/fhir/v2/0078",
            "code": "L",
            "display": "Below low normal"
            }
            ],
            "text": "low"
            }
        ],
  "bodySite": {
    "coding": [
      {
        "system": "http://snomed.info/sct",
        "code": "368209003",
        "display": "Right arm"
      }
    ]
  },
  "component": [
    {
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "8480-6",
            "display": "Systolic blood pressure"
          },
          {
            "system": "http://snomed.info/sct",
            "code": "271649006",
            "display": "Systolic blood pressure"
          },
          {
            "system": "http://acme.org/devices/clinical-codes",
            "code": "bp-s",
            "display": "Systolic Blood pressure"
          }
        ]
      },
      "valueQuantity": {
        "value": 107,
        "unit": "mm[Hg]"
      }
    },
    {
      "code": {
        "coding": [
          {
            "system": "http://loinc.org",
            "code": "8462-4",
            "display": "Diastolic blood pressure"
          }
        ]
      },
      "valueQuantity": {
        "value": 60,
        "unit": "mm[Hg]"
      }
    }
  ]
}
obs = Observation(json)

# print the observation as a JSON object
print(obs.as_json())
