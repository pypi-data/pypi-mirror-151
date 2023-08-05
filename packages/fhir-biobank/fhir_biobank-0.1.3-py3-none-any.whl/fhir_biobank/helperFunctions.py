from typing import List

import fhirclient.models.coding as _fhirclient_coding
import fhirclient.models.codeableconcept as _fhirclient_codeableconcept
import fhirclient.models.identifier as _fhirclient_identifier
import fhirclient.models.fhirreference as _fhirclient_fhirreference
from fhir_biobank._Constants import IDENTIFIER_USE as _IDENTIFIER_USE
from fhir_biobank._Constants import IDENTIFIER_TYPE_CODES as \
    _IDENTIFIER_TYPE_CODES
from fhir_biobank._Constants import IDENTIFIER_CODES_SYSTEM as \
    _IDENTIFIER_CODES_SYSTEM

__all__ = ["Helper"]


class Helper:
    """
        This class defines static methods that are used in converting Classes
        and their information into a FHIR representation, and creating correct
        codes and codeable concepts for FHIR representation of the resources.
    """

    @staticmethod
    def create_coding(code: str, system: str = None, version: str = None,
                      display: str = None,
                      user_selected: bool = True):
        """
         This method creates a reference to a code defined by a
         terminology system.

        :param string code:
            Symbol in syntax defined by the system. This symbol can be
            predefined code or and expression defined by the coding system.
            See for example IDENTIFIER_TYPE_CODES
        :param string system:
            the identification of the code system that defines the meaning of
            symbol in the code
        :param string version:
            the version of the code system which was used when choosing this code.
        :param string display:
            representation of the meaning of the code in the system
        :param bool user_selected:
            true/false value indicating if the coding was chosen by user directly
            for example: off a pick list of available items (codes or displays.)

        :return: FHIR Coding resource

        :raise TypeError: This exception is raised when incorrect
                          types of arguments are provided
        """
        if not isinstance(code, str):
            raise TypeError("code has to be a string!")

        if system is not None and not isinstance(system, str):
            raise TypeError("system has to be a string!")

        if version is not None and not isinstance(version, str):
            raise TypeError("version has to be a string!")

        if display is not None and not isinstance(display, str):
            raise TypeError("display has to be a string!")

        if not isinstance(user_selected, bool):
            raise TypeError("user_selected has to be a boolean!")

        coding = _fhirclient_coding.Coding()
        coding.code = code
        coding.system = system
        coding.version = version
        coding.display = display
        coding.userSelected = user_selected
        return coding

    @staticmethod
    def create_codeable_concept(
            list_of_codings: List[_fhirclient_coding.Coding],
            text: str = None):
        """
        This method creates a CodeableConcept - reference to a terminology
        or a text. List of  coding resources is required to
        create a codeable concept.

        :param List[Coding] list_of_codings:
            A reference to a code defined by a terminology system
        :param string text:
            A human language representation of the code

        :return: FHIR CodeableConcept

        :raise TypeError: This exception is raised when incorrect
                          types of arguments are provided

        :raise ValueError: This exception is raised when incorrect
                           value in argument is provided
        """
        if not isinstance(list_of_codings, list):
            raise TypeError(
                "list_of_codings has to be list that contains codings!")
        if len(list_of_codings) == 0:
            raise ValueError("list_of_codings cannot be an empty list!")
        for code in list_of_codings:
            if not isinstance(code, _fhirclient_coding.Coding):
                raise TypeError(
                    "list_of_codings must contain items that "
                    "are type of  Code only!")

        if text is not None and not isinstance(text, str):
            raise TypeError("text has to be string!")

        codeable_concept = _fhirclient_codeableconcept.CodeableConcept()
        codeable_concept.coding = list_of_codings
        codeable_concept.text = text
        return codeable_concept

    @staticmethod
    def create_identifier(value: str, use: str = "usual",
                          identifier_type: str = "ACSN"):
        """
        this function creates an identifier for a resource.
        Identification number is encouraged to use as a value.

        :param string value:
            value of identifier. Identification number is encouraged to use
        :param Optional[string] use:
            purpose of this identifier. default value is "usual".
            correct values are : "usual", "official", "temp",
            "secondary", "old"
        :param Optional[string] identifier_type:
            a coded type for the identifier that can be used to
            determine specific purpose of the identifier. default value is "MR"
            correct values are : "DL", "PPN", "BRN", "MR", "MCN", "EN", "TAX",
            "NIIP","PRN", "MD", "DR", "ACSN", "UDI", "SNO", "SB",
            "PLAC", "FILL", "JHN".
            For more info see
            https://simplifier.net/packages/hl7.fhir.r4.core/4.0.1/files/82653

        :return: Identifier used in resources

        :raise TypeError: This exception is raised when incorrect
                          types of arguments are provided

        :raise ValueError: This exception is raised when incorrect
                           value in argument is provided
        """
        if not isinstance(value, str):
            raise TypeError("value has to be a string!")
        if not isinstance(use, str):
            raise TypeError("use has to be a string!")
        if use not in _IDENTIFIER_USE:
            raise Exception(
                "{} in use is not a correct type!"
                "use type has to be one of the following".format(
                    use) +
                " ".join(
                    ["{}"] * len(_IDENTIFIER_USE)).format(
                    *_IDENTIFIER_USE))
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

        identifier = _fhirclient_identifier.Identifier()

        type_code = Helper.create_coding(identifier_type,
                                         system=_IDENTIFIER_CODES_SYSTEM)
        type_codeable_concept = Helper.create_codeable_concept([type_code])
        identifier.value = value
        identifier.use = use
        identifier.type = type_codeable_concept

        return identifier

    @staticmethod
    def create_fhir_reference(reference: str):
        """
        This method creates correct FHIR object that represents
        a reference to another FHIR object. For example SpecimenResource
        uses reference on PatientResource to indicate that the collected
        specimen comes from the referenced patient.

        :param string reference:
            String that references resource. for example. "Patient/patient.id"

        :return: FHIRReference obtaining provided reference.
        """
        if not isinstance(reference, str):
            raise TypeError(
                "reference needs to be string that works as "
                "Literal reference, Relative, internal or absolute URL.")
        fhir_reference = _fhirclient_fhirreference.FHIRReference()
        fhir_reference.reference = reference
        return fhir_reference
