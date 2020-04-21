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
#print(dataset)

# this is an example of how to extract a single element
acn = dataset[0x0008,0x0050]
#print(acn)

# import an XML parser
# requires "pip3.8 install untangle"
import untangle

# define a resource using XML, just to figure out how to extract values
xml = '''
<measurement>
    <valueQuantity value="107" unit="mmHg" system="http://unitsofmeasure.org" code="mm[Hg]"/>
</measurement>
'''
print(xml)

# extract some values, just to show how its done.  its very easy using untangle
doc = untangle.parse(xml)
print(doc.measurement.valueQuantity['value'])
print(doc.measurement.valueQuantity['unit'])
print(doc.measurement.valueQuantity['system'])
print(doc.measurement.valueQuantity['code'])

# create a observation template.
# this is my second attempt at defining a fhir resource
# in my first attempt, i used a bunch fhir resources that allowed
# me to define fhir resources using python, but that turned out to be
# rather complex and error prone.  perhaps this is no less error prone,
# but it seems much easier to read.
# we include a bunch of variables (e.g. $acn) that will be replaced
# with their actual values (e.g. accession number).

obs = '''
{
    "resourceType" : "Observation", /* formal name for Observation fHIR resource */
    "identifier" : [
        {
            "id" : {
                "system" : "urn:ietf:rfc:3986",
                "value" : "urn:uuid:$uuid" /* $uuid replaced by uniquely generated uuid4 */
            }
        }
    ],
    "partOf" : [ /* references imaging study, using SIUID and ACN */
        {
            "identifier" : {
                "system" : "urn:dicom:uid",
                "value" : "urn:oid:$siuid" /* $siuid replaced by study instance uid */
            },
            "type" : "ImagingStudy"
        },
        {
            "identifier" : {
                "system" : "http:grh.org/accession",
                "type" : {
                    "coding": [
                        {
                            "code" : "ACSN",
                            "system" : "http://terminology.hl7.org/CodeSystem/v2-0203"
                        }
                    ]
                },
                "value" : "$acn" /* $acn replaced by accession number */
            }
        }
    ],
    "status" : "final", /* copied from teri's sample */
    "category" : { /* copied from teri's sample */
        "system" : "http://hl7.org/fhir/ValueSet/observation-category",
        "version" : "4.0.1",
        "code" : "imaging",
        "display" : "Imaging"
    },
    "code" : { /* need actual LOINC codes or codes from other system */
        "coding" : [
            {
                "system" : "http://loinc.org",
                "code" : "TBD", /* need LOINC code */
                "display" : "TBD" /* need LOINC display */
            }
        ]
    },
    "subject" : {
        "reference" : "Patient/$pid", /* will replace $pid with patient id */
        "display": "$givenname $familyname" /* will replace $givenname and $familyname with given and family name */
    },
    "encounter" : {}, /* anything to do here? */
    "effectiveDateTime" : {}, /* need to put study date and time here */
    "performer" : {}, /* what do we want to reference here? */
    "valueCodeableConcept" : [ /* SNOMED codes for COVID-19 */
        {
            "system": "",
			"code": "",
			"display": ""
        }
	],
    "interpretation" : [ /* abnormal or thickened */
        {
            "system": "",
			"code": "",
			"display": ""
        }
	],
    "bodySite" : [ /* need code for lungs */
        {
            "system": "",
			"code": "",
			"display": ""
        }
	],
    "method" : [ /* US */
        {
            "system": "",
			"code": "",
			"display": ""
        }
	],
    "device" : {}, /* what do we reference here, if anything? */
    "derivedFrom" : [ /* references imaging study, using SIUID and ACN */
        {
            "identifier" : {
                "system" : "urn:dicom:uid",
                "value" : "urn:oid:$siuid" /* $siuid replaced by study instance uid */
            },
            "type" : "ImagingStudy"
        },
        {
            "identifier" : {
                "system" : "http:grh.org/accession",
                "type" : {
                    "coding": [
                        {
                            "code" : "ACSN",
                            "system" : "http://terminology.hl7.org/CodeSystem/v2-0203"
                        }
                    ]
                },
                "value" : "$acn" /* $acn replaced by accession number */
            }
        }
    ],
    "component" : [
        { /* right upper lung */
            "code" : [
                {
                    "system": "",
        			"code": "", /* need code */
        			"display": ""
                }
            ],
            "valueQuantity" : {
                "value" : 0, /* need value */
                "comparator" : "", /* do we need this? */
                "unit" : "", /* need unit */
                "system" : "<uri>", /* need uri? */
                "code" : "" /* need code */
            },
            "interpretation" : [ /* do we want to use this? */
                {
                    "system": "",
                    "code": "",
                    "display": ""
                }
            ]
        },
        { /* right mid lung 2 */
            "code" : [
                {
                    "system": "",
        			"code": "", /* need code */
        			"display": ""
                }
            ],
            "valueQuantity" : {
                "value" : 0, /* need value */
                "comparator" : "", /* do we need this? */
                "unit" : "", /* need unit */
                "system" : "<uri>", /* need uri? */
                "code" : "" /* need code */
            },
            "interpretation" : [ /* do we want to use this? */
                {
                    "system": "",
                    "code": "",
                    "display": ""
                }
            ]
        }
    ]
}
'''

# remove the comments

import re
obs = re.sub('/\*.*\*/', '', obs)
obs = re.sub('//.*$', '', obs)

# replace the variables

import uuid
uuid = uuid.uuid4()
obs = obs.replace('$uuid', str(uuid))

siuid = dataset[0x0020,0x000D]
obs = obs.replace('$siuid', siuid.value)

acn = dataset[0x0008,0x0050]
obs = obs.replace('$acn', acn.value)

pid = dataset[0x0010,0x0020]
obs = obs.replace('$pid', pid.value)

pname = dataset[0x0010,0x0010]
obs = obs.replace('$familyname', pname.value.family_name)
obs = obs.replace('$givenname', pname.value.given_name)

# print the observation
print(obs)
