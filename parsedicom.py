import pydicom

dataset = pydicom.dcmread('/Users/Rick/data/dicom/GENECG.dcm')
print(dataset)
acn = dataset[0x0008,0x0050]
print(acn)
