from datetime import datetime, date

import fhirclient.models.meta as _fhirclient_meta
import fhirclient.models.condition as _fhirclient_condition
import fhirclient.models.fhirdate as _fhirclient_date

from fhir_biobank.patient import PatientResource
from fhir_biobank._Constants import META_PROFILE_URL as _META_PROFILE_URL
from fhir_biobank._Constants import  ICD_CODING_SYSTEM as _ICD_CODING_SYSTEM
from fhir_biobank.helperFunctions import Helper

__all__ = ["ConditionResource"]


class ConditionResource:
    """
    This class represents medical condition or diagnosis of a patient.
    """

    def __init__(self, condition_id: str, condition_code: str,
                 starting_date_condition: date,
                 patient: PatientResource):
        """
        :param string condition_id:
            Internal id that represents unique Condition,
            and is used for references to other resources
        :param string condition_code:
            Code that represents condition, problem, or diagnosis.
        :param date starting_date_condition:
            estimated or actual date or the condition began, in
            opinion of a clinician
        :param PatientResource patient:
            Indicates which patient is associated with the condition.

        :raise TypeError: This exception is raised when incorrect
            Types of arguments are provided.
        :raise ValueError: This exception is raised when incorrect
            value inside argument is provided.
        """
        if not isinstance(condition_id, str):
            raise TypeError("condition_id has to be a string!")

        if not isinstance(starting_date_condition, date):
            raise TypeError("starting_date_condition has to be a datetime!")
        if starting_date_condition > datetime.today().date():
            raise ValueError(
                "starting_date_condition cannot be greater than today!")
        if not isinstance(condition_code, str):
            raise TypeError("condition_code has to be a string!")
        if not isinstance(patient, PatientResource):
            raise TypeError("patient has to be a PatientResource!")

        self._conditionId = condition_id
        self._conditionCode = condition_code
        self._startingDateCondition = starting_date_condition
        self._patient = patient

        self._FHIRCondition = None

    @property
    def conditionId(self):
        """
        Getter for a internal id that represents unique Condition.

        :return: internal id of the Condition resource
        """
        return self._conditionId

    @property
    def conditionCode(self):
        """
        Getter for condition code - code that represents condition,
        problem or diagnosis.

        :return: Code that represents condition, problem, or diagnosis.
        """
        return self._conditionCode

    @property
    def startingDateCondition(self):
        """
        Getter for a date that the condition began.

        :return: date when the condition began
        """
        return self._startingDateCondition

    @property
    def patient(self):
        """
        Getter for a patient that is associated with the condition.

        :return: PatientResource that is associated to the condition
        """
        return self._patient

    @property
    def FHIRInterpretation(self):
        """
        Getter for a FHIR object that is created from this Class.

        :return: Condition in a correct FHIR interpretation.
        """
        if self._FHIRCondition is None:
            self._FHIRCondition = self._convert_to_FHIR()
        return self._FHIRCondition

    def conditionJSON(self):
        """
        Method that creates JSON representation of a Condition Resource.

        :return: FHIR condition resource interpreted as a json format.
        """
        if self._FHIRCondition is None:
            self._FHIRCondition = self._convert_to_FHIR()
        return self._FHIRCondition.as_json()

    def _convert_to_FHIR(self):
        """
        private function to create a FHIR representation of condition
        used in self.conditionJson() and self.FHIRInterpretation()
        """
        condition = _fhirclient_condition.Condition()

        condition.meta = _fhirclient_meta.Meta()
        condition.meta.profile = [_META_PROFILE_URL["Condition"]]

        coding = Helper.create_coding(self._conditionCode, _ICD_CODING_SYSTEM,
                                      user_selected=False)
        codeable_concept = Helper.create_codeable_concept([coding])

        fhir_date = _fhirclient_date.FHIRDate()
        fhir_date.date = self._startingDateCondition

        subject = Helper.create_fhir_reference(
            "patient/" + self._patient.patientId)

        condition.id = self.conditionId
        condition.code = codeable_concept
        condition.onsetDateTime = fhir_date
        condition.subject = subject
        return condition

