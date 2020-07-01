import pandas as pd
from urllib.parse import urlencode
import requests

# WIP


class BioGrid:
    def __init__(self, access_key):
        self.key = access_key
        self.base_url = "https://webservice.thebiogrid.org/"
        self.interactions = "interactions/?"
        self.valid_keys = [
            "start",
            "max",
            "interSpeciesExcluded",
            "selfInteractionsExcluded",
            "evidenceList",
            "includeEvidence",
            "geneList",
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

    def __make_url(self, params):
        info = (("accessKey", self.key), ("format", "json"))
        params = self.__valid_keywords(params)
        params = tuple({(k, v) for k, v in params.items()})
        url = params + info
        encoded = urlencode(url, safe="|")
        endpoint = self.base_url + self.interactions + encoded
        return endpoint

    def get_interactions(self, **kwargs):
        endpoint = self.__make_url(kwargs)
        req = requests.get(endpoint).json()
        inter_table = pd.DataFrame(req).T.reset_index(drop=True)
        return inter_table

    def __valid_keywords(self, params):

        for param in params.keys():
            if param not in self.valid_keys:
                raise ValueError(
                    f"{param} is not a valid argument, check the valid_keys attribute to see a list of them."
                )
            elif param == "geneList":
                # Checking the intersection
                if set(params.keys()) & set(self.valid_keys[7:10]):
                    params[param] = "|".join(params[param])
                else:
                    raise ValueError(
                        f"If you pass a gene list, you have to pass one of these three arguments {self.valid_keys[7:10]} as true, to indicate which ids you're using."
                    )

        return params


import os

test = BioGrid(access_key=os.environ.get("ACCESS_KEY")).get_interactions(
    searchNames=True, geneList=["MAPK10", "BRCA1"]
)

print(test)
