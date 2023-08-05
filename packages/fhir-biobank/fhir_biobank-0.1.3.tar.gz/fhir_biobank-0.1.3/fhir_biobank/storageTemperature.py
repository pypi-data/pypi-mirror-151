from fhir_biobank._Constants import STORAGE_TEMPERATURE_CODES as \
    _STORAGE_TEMPERATURE_CODES
from fhir_biobank._Constants import STORAGE_TEMPERATURE_EXTENSION_URL as \
    _STORAGE_TEMPERATURE_EXTENSION_URL
from fhir_biobank._Constants import STORAGE_TEMPERATURE_SYSTEM as \
    _STORAGE_TEMPERATURE_SYSTEM
from fhir_biobank.helperFunctions import Helper as _Helper

import fhirclient.models.extension as _fhirclient_extension

__all__ = ["StorageTemperature"]


class StorageTemperature:
    """
        This class represents extension that specifies code in
        which temperature was the sample kept at.
        It is is used in specimen resources (parameter extensions.)
        URL of the extension is already provided.
    """

    def __init__(self, storage_temperature_code: str):
        """
        :param string storage_temperature_code: code of the temperature that
            the sample was stored in. Available codes are at
            https://simplifier.net/bbmri.de/storagetemperature
        """
        if not isinstance(storage_temperature_code, str):
            raise TypeError("storage_temperature_code has to be string!")
        if storage_temperature_code not in _STORAGE_TEMPERATURE_CODES:
            raise Exception(
                "{} in storage_temperature_code is not correct "
                "code for storage temperature."
                "Code has to be one of the following: ".format(
                    storage_temperature_code) +
                " ".join(["{}"] * len(_STORAGE_TEMPERATURE_CODES)).format(
                    *_STORAGE_TEMPERATURE_CODES))

        self._storage_temperature_code = storage_temperature_code
        self._storage_temperature_url = _STORAGE_TEMPERATURE_EXTENSION_URL

        storage_temp_coding = _Helper.create_coding(storage_temperature_code,
                                                    _STORAGE_TEMPERATURE_SYSTEM
                                                    , user_selected=False)
        storage_temp_codeable_concept = _Helper.create_codeable_concept(
            [storage_temp_coding])

        self._extension = _fhirclient_extension.Extension()
        self._extension.url = self._storage_temperature_url
        self._extension.valueCodeableConcept = storage_temp_codeable_concept

    @property
    def storageTemperatureCode(self):
        """
        Gettter for a Code that indicates in which temperature the sample
        was stored in.

        :return:Code of the storage temperature
        """
        return self._storage_temperature_code

    @property
    def storageTemperatureUrl(self):
        """
        Getter for URL that defines storage temperature extension.

        :return: URL to a definition of a storage temperature extension.
        """
        return self._storage_temperature_url

    @property
    def fhirExtension(self):
        """
        Getter for a storage temperature extension
        interpreted as a FHIR extension.

        :return: FHIR StorageTemeperature extension in a correct FHIR representation.
        """
        return self._extension
