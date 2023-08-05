from datetime import date, datetime
from typing import List, Union

from fhir_biobank.custodian import Custodian
from fhir_biobank.diagnosis import Diagnosis
from fhir_biobank.storageTemperature import StorageTemperature
from fhir_biobank.patient import PatientResource
from fhir_biobank._Constants import SPECIMEN_TYPE as _SPECIMEN_TYPE
from fhir_biobank._Constants import META_PROFILE_URL as _META_PROFILE_URL
from fhir_biobank._Constants import BODY_SITE_SYSTEM as _BODY_SITE_SYSTEM
from fhir_biobank._Constants import SPECIMEN_QUANTITY_SYSTEM as \
    _SPECIMEN_QUANTITY_SYSTEM
from fhir_biobank._Constants import SPECIMEN_TYPE_SYSTEM as \
    _SPECIMEN_TYPE_SYSTEM
from fhir_biobank._Constants import IDENTIFIER_TYPE_CODES as \
    _IDENTIFIER_TYPE_CODES
import fhirclient.models.specimen as _fhirclient_specimen
import fhirclient.models.meta as _fhirclient_meta
import fhirclient.models.fhirdate as _fhirclient_date
import fhirclient.models.quantity as _fhirclient_quantity

from fhir_biobank.helperFunctions import Helper as _Helper

__all__ = ["SpecimenResource"]


class SpecimenResource:
    """
    This class represents all the necessary information needed for a sample to
    be used for analysis.
    """

    def __init__(self, specimen_id: str, identifier: str,
                 specimen_material_code: str,
                 subject: PatientResource,
                 collected_date: date,
                 quantity: float,
                 body_site_collection_code: str = None,
                 quantity_unit: str = None,
                 quantity_unit_code: str = None,
                 extensions: List[Union[
                     Diagnosis, Custodian, StorageTemperature]] = None,
                 identifier_type: str = "ACSN"):
        """
        :param string specimen_id:
            Internal id that represents unique specimen,
            and is used for references to other resources
        :param string identifier:
            used to uniquely identify specimen inside
            the transactions between biobanks.
        :param string specimen_material_code:
            Type of material that forms the specimen. Correct values are:
            "whole-blood", "bone-marrow", "buffy-coat", "dried-whole-blood",
            "peripheral-blood-cells-vital", "blood-plasma", "plasma-edta",
            "plasma-citrat", "plasma-heparin", "plasma-cell-free",
            "plasma-other", "blood-serum", "ascites", "csf-liquor", "saliva",
            "stool-faeces","urine", "swab", "liquid-other", "tissue-ffpe",
            "tumor-tissue-ffpe", "normal-tissue-ffpe", "other-tissue-ffpe",
            "tissue-frozen", "tumor-tissue-frozen", "normal-tissue-frozen",
            "other-tissue-frozen", "tissue-other", "dna", "cf-dna", "g-dna",
            "rna", "derivative-other"
        :param PatientResource subject:
            class "PatientResource" representing patient from which
            the specimen was taken.
        :param string body_site_collection_code:
            Code of the location that the specimen was collected from.
            Code comes from SNOMED CT
        :param date collected_date:
            Time when specimen was collected from patient.
        :param float quantity:
            quantity of specimen.
        :param string quantity_unit:
            Unit of measure for quantity.
        :param string quantity_unit_code:
            UCUM code of the quantity unit
        :param List[Union[Diagnosis, Custodian, StorageTemperature]] extensions:
            List of extensions that provide addition information
            about the specimen. For example StorageTemperature provides
            additional info about how the specimen is stored
        :param Optional[string] identifier_type:
            a coded type for the identifier that can be used to
            determine specific purpose of the identifier.
            default value is "ACSN"
            correct values are : "DL", "PPN", "BRN", "MR", "MCN", "EN", "TAX",
            "NIIP","PRN", "MD", "DR", "ACSN", "UDI", "SNO", "SB", "PLAC",
            "FILL", "JHN". For more info see
            https://simplifier.net/packages/hl7.fhir.r4.core/4.0.1/files/82653

        :raise TypeError: This exception is raised when incorrect
            types of arguments are provided
        :raise ValueError: This exception is raised when incorrect
            value in argument is provided
        """
        if not isinstance(specimen_id, str):
            raise TypeError("condition_id has to be a string!")

        if not isinstance(identifier, str):
            raise TypeError("identifier has to be string!")
        if not isinstance(specimen_material_code, str):
            raise TypeError("specimen_material_code has to be a string!")
        if specimen_material_code not in _SPECIMEN_TYPE:
            raise ValueError(
                "{} in specimen_type_codeable_concept.coding is not correct "
                "code for specimen."
                "code has to be one of the following".format(
                    specimen_material_code) +
                " ".join(["{}"] * len(_SPECIMEN_TYPE)).format(*_SPECIMEN_TYPE))

        if not isinstance(subject, PatientResource):
            raise TypeError(
                "subject has to be Patient_Resource - patient from which "
                "specimen was taken!")
        if body_site_collection_code is not None and not isinstance(
                body_site_collection_code, str):
            raise TypeError("body_site_collection_code has to be a string!")

        if not isinstance(collected_date, date):
            raise TypeError("collected_date_time has to be a datetime!")

        if collected_date > datetime.today().date():
            raise ValueError(
                "collected_date_time cannot be greater than today's date! ")
        if not isinstance(quantity, float):
            raise TypeError("quantity has to be a float!")

        if quantity_unit is not None and not isinstance(quantity_unit, str):
            raise TypeError("quantity_unit has to be a string!")

        if quantity_unit_code is not None and not isinstance(
                quantity_unit_code,
                str):
            raise TypeError("quantity_unit_code has to be a string!")

        if extensions is not None and not isinstance(extensions, List):
            raise TypeError("extensions has to be List or None!")
        if extensions is not None:
            if len(extensions) == 0:
                raise ValueError("extensions cannot be an empty list!")
            for extension in extensions:
                if not isinstance(extension, StorageTemperature) \
                        and not isinstance(extension, Diagnosis) \
                        and not isinstance(extension, Custodian):
                    raise TypeError(
                        "Extensions have to be one of the following:"
                        " StorageTemperature, Diagnosis or Custodian")

        if not isinstance(identifier_type, str):
            raise TypeError("identifier_type has to be a string!")

        if identifier_type not in _IDENTIFIER_TYPE_CODES:
            raise Exception(
                "{} in identifier_type is not a correct type!"
                "identifier type has to be one of the following".format(
                    identifier_type) +
                " ".join(
                    ["{}"] * len(_IDENTIFIER_TYPE_CODES)).format(
                    *_IDENTIFIER_TYPE_CODES))

        self._specimenId = specimen_id
        self._identifier = identifier
        self._specimenMaterialCode = specimen_material_code
        self._subject = subject
        self._bodySiteCollectionCode = body_site_collection_code
        self._collectedDate = collected_date
        self._quantity = quantity
        self._quantityUnit = quantity_unit
        self._quantityUnitCode = quantity_unit_code
        self._extensions = extensions
        self._identifierType = identifier_type

        self._FHIRSpecimen = None

    @property
    def specimenId(self):
        """
        Getter for a internal id that represents unique Specimen.

        :return: str
            internal id used for references to other resources
        """
        return self._specimenId

    @property
    def identifier(self):
        """
        Getter for identifier of the specimen.

        :return: Identifier of the specimen
        """
        return self._identifier

    @property
    def specimenMaterialCode(self):
        """
        Getter for specimen material code - code that defines type of material
        which forms specimen.

        :return: Code of the material
        """
        return self._specimenMaterialCode

    @property
    def subject(self):
        """
        Getter for a subject - PatientResource that the specimen comes from.

        :return: PatientResource indicating patient from which
            the specimen comes from
        """
        return self._subject

    @property
    def bodySiteCollectionCode(self):
        """
        Getter for a body site collection code - code that defines from which
        part of the body the specimen was taken from.

        :return: Code of the body site
        """
        return self._bodySiteCollectionCode

    @property
    def collectedDateTime(self):
        """
        Getter for a collected date.
        Indicates date which the specimen was taken.

        :return: date of the specimen collection
        """
        return self._collectedDate

    @property
    def quantity(self):
        """
        Getter for a quantity of the specimen.

        :return: quantity of the specimen
        """
        return self._quantity

    @property
    def quantityUnit(self):
        """
        Getter for a unit that the quantity is measured with.

        :return: unit that the quantity is measured with
        """
        return self._quantityUnit

    @property
    def quantityUnitCode(self):
        """
        Getter for a code that defines the quantityUnit.

        :return: code of the unit that the quantity is measured with
        """
        return self._quantityUnitCode

    @property
    def extensions(self):
        """
        Getter for list of extensions - additional information
        about the specimen.

        :return: List of extensions.
        """
        return self._extensions

    @property
    def identifierType(self):
        """
        Getter for a type of the indentifier that identifies the specimen.

        :return: code for the type of identifier
        """
        return self.identifierType

    @property
    def FHIRInterpretation(self):
        """
        Getter for a FHIR object that is created from this class.

        :return: Specimen in a correct FHIR interpretation
        """
        if self._FHIRSpecimen is None:
            self._FHIRSpecimen = self._convert_to_FHIR()
        return self._FHIRSpecimen

    def specimenJSON(self):
        """
        Method that creates JSON representation of a Specimen Resource.

        :return: FHIR Specimen resource represented in a json format.
        """
        if self._FHIRSpecimen is None:
            self._FHIRSpecimen = self._convert_to_FHIR()
        return self._FHIRSpecimen.as_json()

    def _convert_to_FHIR(self):
        """
            private function to create a FHIR representation of specimen
            used in self.patientJson() and self.FHIRInterpretation()

            :return: fhirclient.models.specimen.Specimen
        """
        FHIR_specimen = _fhirclient_specimen.Specimen()

        FHIR_specimen.id = self._specimenId

        FHIR_specimen.identifier = [
            _Helper.create_identifier(self._identifier,
                                      identifier_type=self._identifierType)]
        FHIR_specimen.meta = _fhirclient_meta.Meta()
        FHIR_specimen.meta.profile = [_META_PROFILE_URL["Specimen"]]

        fhir_specimen_type_coding = _Helper.create_coding(
            self._specimenMaterialCode,
            _SPECIMEN_TYPE_SYSTEM, user_selected=False)
        fhir_specimen_type_codeable_concept = _Helper.create_codeable_concept(
            [fhir_specimen_type_coding])

        collection = _fhirclient_specimen.SpecimenCollection()

        fhir_collected_time = _fhirclient_date.FHIRDate()
        fhir_collected_time.date = self._collectedDate

        # TODO collection coding system ?
        #  is not defined in simplifier (Question) ?
        if self._bodySiteCollectionCode is not None:
            fhir_body_site_collection_coding = _Helper.create_coding(
                self._bodySiteCollectionCode, _BODY_SITE_SYSTEM,
                user_selected=False)
            fhir_body_site_collection_codeable_concept = \
                _Helper.create_codeable_concept(
                    [fhir_body_site_collection_coding])
            collection.bodySite = fhir_body_site_collection_codeable_concept

        collection.collectedDateTime = fhir_collected_time

        subject_reference = _Helper.create_fhir_reference(
            "Patient/" + self._subject.patientId)

        container = _fhirclient_specimen.SpecimenContainer()
        quantity = _fhirclient_quantity.Quantity()
        quantity.value = self._quantity
        quantity.unit = self._quantityUnit
        quantity.code = self._quantityUnitCode
        quantity.system = _SPECIMEN_QUANTITY_SYSTEM
        container.specimenQuantity = quantity

        extensions = None
        if self._extensions is not None:
            extensions = []
            for extension in self._extensions:
                extensions.append(extension.fhirExtension)

        FHIR_specimen.type = fhir_specimen_type_codeable_concept
        FHIR_specimen.collection = collection
        FHIR_specimen.subject = subject_reference
        FHIR_specimen.container = [container]
        FHIR_specimen.extension = extensions
        return FHIR_specimen
