from fhir_biobank._Constants import DIAGNOSIS_EXTENSION_URL as \
    _DIAGNOSIS_EXTENSION_URL
from fhir_biobank._Constants import ICD_CODING_SYSTEM as _ICD_CODING_SYSTEM
from fhir_biobank.helperFunctions import Helper

import fhirclient.models.extension as _fhirclient_extension

__all__ = ["Diagnosis"]


class Diagnosis:
    """
        This class represents extension that specifies code of diagnosis that
        the patient (from which the sample was taken) has. URL of the extension
        is already provided.
    """

    def __init__(self, diagnosis_code: str):
        """
        :param diagnosis_code: code of the diagnosis that the patient has.
            System which defines these codes is ICD-10. You can look up
            the codes at https://www.icd10data.com/ICD10CM/Codes
        """
        if not isinstance(diagnosis_code, str):
            raise TypeError("diagnosis_code has to be string!")

        self._diagnosisCode = diagnosis_code
        self._diagnosisUrl = _DIAGNOSIS_EXTENSION_URL

        diagnosis_coding = Helper.create_coding(diagnosis_code,
                                                _ICD_CODING_SYSTEM,
                                                user_selected=False)

        diagnosis_codeable_concept = Helper.create_codeable_concept(
            [diagnosis_coding])

        self._extension = _fhirclient_extension.Extension()
        self._extension.url = self._diagnosisUrl
        self._extension.valueCodeableConcept = diagnosis_codeable_concept

    @property
    def fhirExtension(self):
        """
        Getter for a Diagnosis extension interpreted as a FHIR extension.

        :return: FHIR Diagnosis extension in a correct FHIR representation.
        """
        return self._extension

    @property
    def diagnosisCode(self):
        """
        Getter for a code of the diagnosis
        defined at https://www.icd10data.com/ICD10CM/Codes

        :return: Code of the diagnosis
        """
        return self._diagnosisCode

    @property
    def diagnosisUrl(self):
        """
        Getter for URL that defines diagnosis extension.

        :return: URL to a definition of a diagnosis extension.
        """
        return self._diagnosisUrl
