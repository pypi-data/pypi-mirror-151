from typing import List, Union
import fhirclient.models.bundle as _fhirclient_bundle

from fhir_biobank.condition import ConditionResource as ConditionResource
from fhir_biobank.patient import PatientResource as PatientResource
from fhir_biobank.specimen import SpecimenResource as SpecimenResource

from fhir_biobank._Constants import BUNDLE_REQUEST_METHOD as \
    _BUNDLE_REQUEST_METHOD
from fhir_biobank._Constants import BUNDLE_TYPES as _BUNDLE_TYPES


__all__ = ["Entry", "Bundle"]


class Entry:
    """
    This class represents an entry in a bundle. Entry contains resource and
    its full and short url.

    """

    def __init__(self, resource: Union[PatientResource, SpecimenResource,
                                       ConditionResource],
                 resource_full_url: str, resource_short_url: str,
                 request_method: str = "PUT"):
        """

        :param [PatientResource, SpecimenResource,ConditionResource] resource:
            resource that an entry will contain. It can be either
            PatientResource, SpecimenResource or a ConditionResource.
        :param string resource_full_url:
            full url of the resource that is in the entry.
            for example: https://example.com/Patient/0
        :param string resource_short_url:
            short (relative) url of the resource that is in the entry.
            for example: Patient/0
        :param string request_method:
            this method indicates desired action to be preformed for a given
            resource. Correct values are: GET PUT POST DELETE

        :raise TypeError: This exception is raised when incorrect
                          types of arguments are provided
        """
        if not isinstance(resource, PatientResource) \
                and not isinstance(resource, SpecimenResource) \
                and not isinstance(resource, ConditionResource):
            raise TypeError("resource type has to be one of the following: "
                            "PatientResource, SpecimenResource or"
                            " ConditionResource")

        if not isinstance(resource_full_url, str):
            raise TypeError("resource_url has to be a string!")

        if not isinstance(request_method, str):
            raise TypeError("request_method has to be a string!")

        if not isinstance(resource_short_url, str):
            raise TypeError("resource_short_url has to be a string!")

        if request_method not in _BUNDLE_REQUEST_METHOD:
            raise TypeError(
                "{} in request_method is not correct method! "
                "request_method has to be one of the following".format(
                    request_method) +
                " ".join(["{}"] * len(_BUNDLE_REQUEST_METHOD)).format(
                    *_BUNDLE_REQUEST_METHOD))

        self._resource = resource.FHIRInterpretation
        self._resourceFullUrl = resource_full_url
        self._resourceShortUrl = resource_short_url
        self._requestMethod = request_method
        self._FHIREntry = None

    @property
    def resource(self):
        """
        Getter for resource property.

        :return: resource that is contained by the entry.
        """
        return self._resource

    @property
    def resourceFullUrl(self):
        """
        Getter for the resource full url.

        :return: Full url of the resource.
        """
        return self._resourceFullUrl

    @property
    def resourceShortUrl(self):
        """
        Getter for the resource short url.

        :return: short url of the resource.
        """
        return self._resourceShortUrl

    @property
    def requestMethod(self):
        """
        Getter for the request method.

        :return: request method indicating desired action
            to be preformed for a given resource.
        """
        return self._requestMethod

    @property
    def FHIRInterpretation(self):
        """
        Getter for a FHIR object that is created from this class.

        :return: Entry in a correct FHIR interpretation

        """
        if self._FHIREntry is None:
            self._FHIREntry = self._convert_to_FHIR()
        return self._FHIREntry

    def entryJSON(self):
        """
        Method that creates JSON representation of an Entry Resource.

        :return: FHIR Entry resource represented in a json format.
        """
        if self._FHIREntry is None:
            self._FHIREntry = self._convert_to_FHIR()
        return self._FHIREntry.as_json()

    def _convert_to_FHIR(self):
        """
        private function to create a FHIR representation of Entry used in

        self.entryJson() and self.FHIRInterpretation()
        """
        FHIREntry = _fhirclient_bundle.BundleEntry()

        entry_request = _fhirclient_bundle.BundleEntryRequest()
        entry_request.url = self._resourceShortUrl
        entry_request.method = self._requestMethod

        FHIREntry.resource = self._resource
        FHIREntry.fullUrl = self._resourceFullUrl
        FHIREntry.request = entry_request
        return FHIREntry


class Bundle:
    """
    This class represents a Bundle - a container for collection of resources.
    Bundle can be used for sending/returning/storing a set of resources,etc.
    """

    def __init__(self, bundle_id: str, entries: List[Entry],
                 bundle_type="transaction"):
        """
        :param string bundle_id:
            Internal id that represents unique Bundle
        :param List[Entry] entries:
            List of Entries that should be included in a Bundle. Each Entry
            contains Resource. Entries represent the collection of resources
            contained in this Bundle.
        :param Optional[str] bundle_type:
            String that indicates the purpose of this Bundle.
            Correct values are: "document", "message", "transaction",
            "transaction-response", "batch", "batch-response", "history",
            "searchset", "collection"

        :raise TypeError: This exception is raised when incorrect
                          types of arguments are provided.
        :raise ValueError: This exception is raised when incorrect
                           value inside argument is provided.
        """
        if not isinstance(bundle_id, str):
            raise TypeError("bundle_id has to be a string! ")

        if not isinstance(entries, List):
            raise TypeError(
                "entries has to be a list containing objects Entry")

        if len(entries) == 0:
            raise ValueError("entries list cannot be empty!")

        for entry in entries:
            if not isinstance(entry, Entry):
                raise TypeError(
                    "entries has to be a list containing objects Entry")

        if not isinstance(bundle_type, str):
            raise TypeError("bundle_type has to be a string!")

        if bundle_type not in _BUNDLE_TYPES:
            raise TypeError("{} in bundle_type is not correct bundle type!"
                            .format(bundle_type) +
                            " ".join(["{}"] * len(_BUNDLE_TYPES))
                            .format(*_BUNDLE_TYPES))

        self._entries = []
        for entry in entries:
            self._entries.append(entry.FHIRInterpretation)

        self._id = bundle_id
        self._bundle_type = bundle_type
        self._FHIRBundle = None

    @property
    def id(self):
        """
        Getter for bundle id - internal id that represents unique Bundle

        :return: String - internal id that represents unique Bundle.
        """
        return self._id

    @property
    def entries(self):
        """
        Getter for a collection of entries already in a FHIR.

        :return: List of Entries that are in a Bundle.
        """
        return self._entries

    @property
    def bundleType(self):
        """
        Getter for a Bundle type that indicates purpose of this Bundle.

        :return:  String that indicates the purpose of this Bundle.
        """
        return self._bundle_type

    def bundleJSON(self):
        """
        Method that creates JSON representation of an Patient Resource.

        :return: FHIR Bundle represented in a json format.
        """
        if self._FHIRBundle is None:
            self._FHIRBundle = self._convert_to_FHIR()
        json = str(self._FHIRBundle.as_json()).replace("True", "true")
        json = json.replace("False", "false")
        return json

    def _convert_to_FHIR(self):
        """
         private function to create a FHIR representation of Bundle used in
         self.bundleJson()
        """
        FHIRBundle = _fhirclient_bundle.Bundle()
        FHIRBundle.id = self._id
        FHIRBundle.entry = self._entries
        FHIRBundle.type = self._bundle_type
        return FHIRBundle

