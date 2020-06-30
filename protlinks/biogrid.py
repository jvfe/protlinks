import pandas as pd
from urllib.parse import urlencode

# WIP


class BioGrid:
    def __init__(self, access_key):
        self.key = access_key
        self.base_url = "https://webservice.thebiogrid.org/"
        self.format = "json"
        self.interactions = "interactions/"
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

    def make_url(self, **kwargs):
        info = (("accessKey", self.key), ("format", self.format))
        params = self.__valid_keywords(kwargs)
        params = tuple({(k, v) for k, v in kwargs.items()})
        url = params + info
        endpoint = urlencode(url)
        print(params)

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
                        f"If you pass a gene list, you have to pass one of these three arguments {self.valid_keys[7:10]} as true"
                    )

        return params


BioGrid(access_key="#keyhere").make_url(searchNames=True, geneList=["bla", "ble"])


# def teste_any(**kwargs):
#     for param in kwargs.keys():
#         if param == "geneList":
#             if set(kwargs.keys()) & set(["searchIds", "searchNames", "searchSynonyms"]):
#                 kwargs[param] = "|".join(kwargs[param])
#                 print(kwargs[param])
#             else:
#                 print("False")


# teste_any(searchNames=True, geneList=["bla", "ble"])

