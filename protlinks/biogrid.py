import pandas as pd
from urllib.parse import urlencode

# WIP


class BioGrid:
    def __init__(self, access_key):
        self.key = access_key
        self.base_url = "https://webservice.thebiogrid.org/"
        self.format = "json"

    def make_url(self, **kwargs):
        info = (("accessKey", self.key), ("format", self.format))
        params = self.__valid_keywords(kwargs)
        params = tuple({(k, v) for k, v in kwargs.items()})
        url = params + info
        endpoint = urlencode(url)
        print(endpoint)

    def __valid_keywords(self, params):
        valid_keys = [
            "start",
            "max",
            "interSpeciesExcluded",
            "selfInteractionsExcluded",
            "evidenceList",
            "includeEvidence" "geneList",
            "searchIds",
            "searchNames",
            "searchSynonyms",
            "searchBiogridIds",
            "additionalIdentifierTypes",
            "excludeGenes",
            "includeInteractors",
            "includeInteractorInteractions",
            "pubmedList",
            "excludePubmeds",
            "htpThreshold",
            "throughputTag",
            "taxId",
            "includeHeader",
            "translate",
        ]

        for param in params.keys():
            if param not in valid_keys:
                raise ValueError(
                    f"{param} is not a valid argument, check https://wiki.thebiogrid.org/doku.php/biogridrest for valid keywords."
                )

        return params


BioGrid(access_key="#keyhere").make_url(inter="bla")

