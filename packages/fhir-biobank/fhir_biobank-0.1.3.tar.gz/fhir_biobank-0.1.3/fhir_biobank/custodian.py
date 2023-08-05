from fhir_biobank._Constants import CUSTODIAN_URL
from fhir_biobank.helperFunctions import Helper

import fhirclient.models.extension as _fhirclient_extension

__all__ = ["Custodian"]


class Custodian:
    """
     This class represents reference to a Organization from which a specimen
     comes from. URL of the extension is already provided.
    """

    def __init__(self, reference: str):
        """
        :param string reference:  short url of a resource, same as in
            Entry Resource defined in bundle. For example custodian/0

        :raise TypeError: This exception is raised when incorrect types of
            arguments are provided.
        """
        if not isinstance(reference, str):
            raise TypeError("reference needs to be a string!")

        self._reference = reference
        self._url = CUSTODIAN_URL
        extension = _fhirclient_extension.Extension()
        extension.url = self._url
        extension.valueReference = Helper.create_fhir_reference(reference)
        self._extension = extension

    @property
    def fhirExtension(self):
        """
        Getter for a Custodian extension interpreted as a FHIR extension

        :return: FHIR Custodian extension in a correct FHIR representation
        """
        return self._extension

    @property
    def reference(self):
        """
        Getter for a reference to a custodian

        :return:  reference to a custodian
        """
        return self._reference

    @property
    def custodianUrl(self):
        """
        Getter for URL that defines how custodian extension should look like.
        :return: URL of custodian extension definition
        """
        return self._url


def __dir__():
    return ['Custodian']
