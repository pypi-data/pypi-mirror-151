from datetime import date as _date
from typing import List, Optional
import fhirclient.models.patient as _fhirclient_patient
import fhirclient.models.fhirdate as _fhirclient_date
import fhirclient.models.meta as _fhirclient_meta

from fhir_biobank.helperFunctions import Helper as _Helper

from fhir_biobank._Constants import PATIENT_GENDER as _PATIENT_GENDER
from fhir_biobank._Constants import META_PROFILE_URL as _META_PROFILE_URL
from fhir_biobank._Constants import IDENTIFIER_TYPE_CODES as \
    _IDENTIFIER_TYPE_CODES


class PatientResource:
    """
    This class containts information about an individual receiving
    health care services.
    """

    def __init__(self, patient_id: str, identifier: str,
                 gender: str = "unknown", birth_date: _date = None,
                 deceased_boolean: bool = False,
                 deceased_datetime: _date = None,
                 multiple_birth_boolean: bool = False,
                 multiple_birth_int: int = None,
                 patient_links: Optional[List["PatientResource"]] = None,
                 identifier_type: str = "ACSN"):
        """
        :param string patient_id:
            Internal id that represents unique Patient,
            and is used for references to other resources
        :param string identifier:
            used to uniquely identify patient.
            Identifier should be social security number.
        :param string gender:
            gender of a person used for administrative purposes.
            Possible entries are "male", "female", "other", "unknown"
        :param date birth_date:
            Birth date of a patient. At least estimated year should be provided
            as a guess.
        :param Optional[bool] deceased_boolean:
            true/false value that represents if patient is deceased
        :param Optional[date] deceased_datetime:
            date of patient's death
        :param Optional[bool] multiple_birth_boolean:
            true/false value that represents if patient comes from
            multiple birth.
        :param Optional[int] multiple_birth_int:
            number that represents the order of birth in the multiple birth.
        :param Optional[List[PatientResource]] patient_links:
            list containing references to other patient resource that concerns
            the same person

        :param Optional[string] identifier_type:
            a coded type for the identifier that can be used to
            determine specific purpose of the identifier.
            default value is "ACSN"
            correct values are : "DL", "PPN", "BRN", "MR", "MCN", "EN", "TAX",
            "NIIP","PRN", "MD", "DR", "ACSN", "UDI", "SNO", "SB",
            "PLAC", "FILL", "JHN".
            For more info see
            https://simplifier.net/packages/hl7.fhir.r4.core/4.0.1/files/82653

        :raise TypeError: This exception is raised when incorrect
                          types of arguments are provided

        :raise ValueError: This exception is raised when incorrect
                           value in argument is provided
        """
        if not isinstance(patient_id, str):
            raise TypeError("condition_id has to be a string!")

        if not isinstance(identifier, str):
            raise TypeError("patient_id has to be string!")

        if not isinstance(gender, str):
            raise TypeError("gender has to be string!")

        if gender not in _PATIENT_GENDER:
            raise ValueError(
                "{} in variable gender is not correct "
                "code for gender."
                "code has to be one of the following".format(
                    gender) +
                " ".join(["{}"] * len(_PATIENT_GENDER)).format(
                    *_PATIENT_GENDER))

        if birth_date is not None and not isinstance(birth_date, _date):
            raise TypeError("birth_date has to be date!")

        if birth_date is not None and birth_date > _date.today():
            raise ValueError(
                "Patient birth date cannot be greater than today's date!")

        if not isinstance(deceased_boolean, bool):
            raise TypeError("deceased_boolean has to be bool!")

        if deceased_datetime is not None and not isinstance(deceased_datetime,
                                                            _date):
            raise TypeError("deceased_datetime has to be date!")

        if not deceased_boolean and deceased_datetime is not None:
            raise ValueError(
                "deceased_boolean is set to False,"
                " but deceased_datetime is not None! ")

        if deceased_datetime is not None and deceased_datetime > _date.today():
            raise ValueError(
                "Patient deceased datetime date cannot be "
                "greater than today's date!")

        if birth_date is not None and deceased_datetime is not None \
                and deceased_datetime < birth_date:
            raise ValueError("Patient cannot be deceased before being born!")

        if not isinstance(multiple_birth_boolean, bool):
            raise TypeError("multiple_birth_boolean has to be bool!")

        if multiple_birth_int is not None and not isinstance(
                multiple_birth_int,
                int):
            raise TypeError("multiple_birth_int has to be int!")

        if not multiple_birth_boolean and multiple_birth_int is not None:
            raise ValueError(
                "multiple_birth_boolean set to False, "
                "but multiple_birth_int is not None!")

        if patient_links is not None:
            if not isinstance(patient_links, list):
                raise TypeError("patient_links have to be list of patients!")
            else:
                for patient in patient_links:
                    if not isinstance(patient, PatientResource):
                        raise TypeError(
                            "patient_links have to be list of patients!")

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

        self._patientId = patient_id

        self._identifier = identifier

        self._gender = gender

        self._birthDate = birth_date

        self._deceasedBoolean = deceased_boolean

        self._deceasedDatetime = deceased_datetime
        self._multipleBirthBoolean = multiple_birth_boolean
        self._multipleBirthInteger = multiple_birth_int

        self._link = patient_links

        self._identifierType = identifier_type
        self._FHIR_Patient = None

    @property
    def patientId(self):
        """
        Getter for a internal id that represents unique Condition

        :return: internal id used for references to other resources
        """
        return self._patientId

    @property
    def identifier(self):
        """
        Getter for identifier of the patient.

        :return: Identifier of the patient.
        """
        return self._identifier

    @property
    def gender(self):
        """
        Getter for a gender of the patient.

        :return: Gender of the patient.
        """
        return self._gender

    @property
    def birthDate(self):
        """
        Getter for a birth date of the patient.

        :return: Birth Date of the patient.
        """
        return self._birthDate

    @property
    def deceasedBoolean(self):
        """
        Getter for a True/False value indicating if the patient is deceased.

        :return: True/False value that indicates if the patient is deceased.
        """
        return self._deceasedBoolean

    @property
    def deceasedDatetime(self):
        """
        Getter for a deceased Date of a patient, if one is provided

        :return: Date of the patient's death.
        """
        return self._deceasedDatetime

    @property
    def multipleBirthBoolean(self):
        """
        Getter for a True/False value that indicates if
        patient comes from multiple birth.

        :return: True/False value that indicates if patient comes from multiple
            birth.
        """
        return self._multipleBirthBoolean

    @property
    def multipleBirthInteger(self):
        """
        Getter for a number that indicates order of the patient's
        birth in the multiple birth, if provided.

        :return: Number that indicates order of the patients birth in multiple
            birth.
        """
        return self._multipleBirthInteger

    @property
    def link(self):
        """
        Getter for a list of links to another PatientResource,
        that references the same patient.

        :return: List of links to another PatientResource
        """
        return self._link

    @property
    def identifierType(self):
        """
        Getter for a type of the indentifier that identifies the patient

        :return: type of identifier that identifies the patient
        """
        return self.identifierType

    @property
    def FHIRInterpretation(self):
        """
        Getter for a FHIR object that is created from this class.

        :return: FHIR Patient Resource object.
        """
        if self._FHIR_Patient is None:
            self._FHIR_Patient = self._convert_to_FHIR()
        return self._FHIR_Patient

    def patientJSON(self):
        """
        Method that creates JSON representation of a Patient Resource.

        :return: Json representation containing all given information of
            FHIR patient resource.
        """
        if self._FHIR_Patient is None:
            self._FHIR_Patient = self._convert_to_FHIR()
        return self._FHIR_Patient.as_json()

    def _create_patient_link(self, patients):
        """
        private function to create link to a resource that represents same
        patient.

        :param patients:
        :return: FHIR PatientLink
        """
        if not isinstance(patients, List):
            raise TypeError("param patients has to be List!")
        patient_links = []
        for patient in patients:
            if not isinstance(patient, PatientResource):
                raise TypeError("patient has to be PatientResource")
            patient_link = _fhirclient_patient.PatientLink()
            patient_link.other = _Helper.create_fhir_reference(
                "patient/" + str(self.identifier))
            patient_link.type = "refer"
            patient_links.append(patient_link)
        return patient_links

    def _convert_to_FHIR(self):
        """
            private function to create a FHIR representation of patient
            used in self.patientJson() and self.FHIRInterpretation()

            :return: None
        """
        if self._FHIR_Patient is None:
            FHIR_Patient = _fhirclient_patient.Patient()

            FHIR_Patient.meta = _fhirclient_meta.Meta()
            FHIR_Patient.meta.profile = [_META_PROFILE_URL["Patient"]]
            identifier = [_Helper.create_identifier(self._identifier,
                                                    identifier_type=
                                                    self._identifierType)]
            FHIR_Patient.id = self._patientId

            FHIR_Patient.identifier = identifier
            FHIR_Patient.gender = self._gender
            if self._birthDate is not None:
                fhir_birth_date = _fhirclient_date.FHIRDate()
                fhir_birth_date.date = self._birthDate
                FHIR_Patient.birthDate = fhir_birth_date

            FHIR_Patient.deceasedBoolean = self._deceasedBoolean
            if self._deceasedDatetime is not None:
                fhir_deceased_datetime = _fhirclient_date.FHIRDate()
                fhir_deceased_datetime.date = self._deceasedDatetime
                FHIR_Patient.deceasedDateTime = fhir_deceased_datetime

            FHIR_Patient.multipleBirthBoolean = \
                self._multipleBirthBoolean
            FHIR_Patient.multipleBirthInteger = \
                self._multipleBirthInteger
            if self.link is not None:
                FHIR_Patient.link = self._create_patient_link(self.link)
            return FHIR_Patient


def __dir__():
    return ['PatientResource']


__all__ = ["PatientResource"]
