"""
all the possible types of Bundle
"""

BUNDLE_TYPES = ["document", "message", "transaction", "transaction-response",
                "batch",
                "batch-response", "history", "searchset", "collection"]

"""
All of the possible request methods used in a Bundle.
"""

BUNDLE_REQUEST_METHOD = ["GET", "POST", "PUT", "DELETE"]

"""
All of the possible genders that the patient can have
"""

PATIENT_GENDER = ["male", "female", "other", "unknown"]

"""
All the possible uses of identifier
"""

IDENTIFIER_USE = ["usual", "official", "temp", "secondary", "old"]

"""All the possible types of identifiers. for more extensive description see 
https://simplifier.net/packages/hl7.fhir.r4.core/4.0.1/files/82653 """

IDENTIFIER_TYPE_CODES = ["DL", "PPN", "BRN", "MR", "MCN", "EN", "TAX", "NIIP",
                         "PRN", "MD", "DR", "ACSN", "UDI", "SNO", "SB", "PLAC",
                         "FILL", "JHN"]

"""
URL that describes identifier type codes
"""
IDENTIFIER_CODES_SYSTEM = "http://terminology.hl7.org/CodeSystem/v2-0203"

"""
All possible types of extension
"""
EXTENSION_TYPES = ["storageTemp", "diagnosis", "custodian"]

"""
URL to a definition of storage temperature extension
"""

STORAGE_TEMPERATURE_EXTENSION_URL = \
    "https://fhir.bbmri.de/StructureDefinition/StorageTemperature"

"""
URL to all the possible values for storage temperature
"""

STORAGE_TEMPERATURE_SYSTEM = \
    "https://simplifier.net/bbmri.de/storagetemperature"

"""
All possible codes for storage temperature
"""

STORAGE_TEMPERATURE_CODES = ["temperature2to10", "temperature-18to-35",
                             "temperature-60to-85", "temperatureGN",
                             "temperatureLN", "temperatureRoom",
                             "temperatureOther"]

"""
URLs that define how these resources should look like
"""

META_PROFILE_URL = {
    "Patient": "https://fhir.bbmri.de/StructureDefinition/Patient",
    "Specimen": "https://fhir.bbmri.de/StructureDefinition/Specimen",
    "Condition": "https://fhir.bbmri.de/StructureDefinition/Condition"}

"""
URL that defines how diagnosis extension should look like
"""
DIAGNOSIS_EXTENSION_URL = \
    "https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis"

"""
URL that defines how custodian extension should look like
"""
CUSTODIAN_URL = "https://fhir.bbmri.de/StructureDefinition/Custodian"

"""
URL to a coding system that defines 
"""

ICD_CODING_SYSTEM = "http://hl7.org/fhir/sid/icd-10"

"""
All the possible values for type of specimen
"""
SPECIMEN_TYPE = ["whole-blood", "bone-marrow", "buffy-coat",
                 "dried-whole-blood", "peripheral-blood-cells-vital",
                 "blood-plasma", "plasma-edta", "plasma-citrat",
                 "plasma-heparin", "plasma-cell-free", "plasma-other",
                 "blood-serum", "ascites", "csf-liquor",
                 "saliva", "stool-faeces",
                 "urine", "swab", "liquid-other", "tissue-ffpe",
                 "tumor-tissue-ffpe",
                 "normal-tissue-ffpe", "other-tissue-ffpe", "tissue-frozen",
                 "tumor-tissue-frozen", "normal-tissue-frozen",
                 "other-tissue-frozen",
                 "tissue-other", "dna", "cf-dna", "g-dna", "rna",
                 "derivative-other"]

"""
URL that defines all the possible values for the type of specimen
"""

SPECIMEN_TYPE_SYSTEM = "https://fhir.bbmri.de/CodeSystem/SampleMaterialType"

"""
All the values taht indicate specimen status
"""

SPECIMEN_STATUS = ["available", "unavailable", "unsatisfactory",
                   "entered-in-error"]
"""
URN that defines body sites for specimen collection
"""
BODY_SITE_SYSTEM = "urn:oid:2.16.840.1.113883.6.43.1"

"""
URL that defines all the possible units of measure for specimen quantity
"""
SPECIMEN_QUANTITY_SYSTEM = "http://unitsofmeasure.org"
