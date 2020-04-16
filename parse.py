import argparse

parser = argparse.ArgumentParser(description='Extracts measurements from DICOM SR as XML and outputs as JSON.')
parser.add_argument("-f", "--file", required=True, type=str, help="The name of the file to parse")
args = parser.parse_args()

file = args.file

dataset = pydicom.dcmread(file)
print(dataset)
acn = dataset[0x0008,0x0050]
print(acn)

str = '<employees><person><name value="Alice"/></person><person><name value="Bob"/></person></employees>'
print(str)
