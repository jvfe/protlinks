import pandas as pd
from urllib.parse import urlencode
import requests


class BioGrid:
    """A class to acquire interaction data from BioGRID

    Attributes:
        access_key: Free personal API key for the BioGRID REST webservice
    """

    def __init__(self, access_key):
        self.key = access_key
        self.base_url = "https://webservice.thebiogrid.org/"
        self.interactions = "interactions/?"
        self.valid_keys = {
            "start": (
                "Query results are numbered from 0. Results fetched will start at this value e.g. start = 50 will skip the the first 50 results. Ignored if using “count” in the format parameter.",
                "Default=0",
            ),
            "max": (
                "Number of results to fetch; this will be ignored if greater than 10,000",
                "Default=10000",
            ),
            "interSpeciesExcluded": (
                "If ‘true’, interactions with interactors from different species will be excluded.",
                "Default=FALSE",
            ),
            "selfInteractionsExcluded": (
                "If ‘true’, interactions with one interactor will be excluded.",
                "Default=FALSE",
            ),
            "evidenceList": (
                "Any interaction evidence with its Experimental System in the list will be excluded from the results unless includeEvidence is set to true.",
                "Default=empty",
            ),
            "includeEvidence": (
                "If set to true, any interaction evidence with its Experimental System in the evidenceList will be included in the result",
                "Default=FALSE",
            ),
            "geneList": (
                "Interactions between genes in this list will be fetched. This parameter is ignored if one of searchIds, searchNames, searchSynonyms is not ‘true’ and additionalIdentifierTypes is empty.",
                "Default=empty",
            ),
            "searchIds": (
                "If ‘true’, the interactor ENTREZ_GENE, ORDERED LOCUS and SYSTEMATIC_NAME (orf) will be examined for a match with the geneList .",
                "Default=FALSE",
            ),
            "searchNames": (
                "If ‘true’, the interactor OFFICIAL_SYMBOL will be examined for a match with the geneList.",
                "Default=FALSE",
            ),
            "searchSynonyms": (
                "If ‘true’, the interactor SYNONYM will be examined for a match with the geneList.",
                "Default=FALSE",
            ),
            "searchBiogridIds": (
                "If ‘true’, the entries in 'GENELIST' will be compared to BIOGRID internal IDS which are provided in all Tab2 formatted files.",
                "Default=FALSE",
            ),
            "additionalIdentifierTypes": (
                "Identifier types on this list are examined for a match with the geneList. Some identifier types search multiple types simultaneously. UNIPROT or UNIPROTKB will search SWISS-PROT/TREMBL/UNIPROT-ACCESSION/UNIPROT-ISOFORM. REFSEQ will search REFSEQ-RNA-GI, REFSEQ-RNA-ACCESSION, REFSEQ-PROTEIN-GI, REFSEQ-PROTEIN-ACCESSION-VERSIONED, REFSEQ-PROTEIN-ACCESSION, REFSEQ-LEGACY. WORMBASE will search WORMBASE and WORMBASE-OLD. ENSEMBL will search ENSEMBL, ENSEMBL GENE, ENSEMBL PROTEIN, ENSEMBL RNA.",
                "Default=empty",
            ),
            "excludeGenes": (
                "If ‘true’, interactions containing genes in the geneList will be excluded from the results. Ignored if one of searchIds, searchNames, searchSynonyms is not ‘true’ and additionalIdentifierTypes is empty.",
                "Default=FALSE",
            ),
            "includeInteractors": (
                "If ‘true’, in addition to interactions between genes on the geneList, interactions will also be fetched which have only one interactor on the geneList i.e. the geneList’s first order interactors will be included",
                "Default=TRUE",
            ),
            "includeInteractorInteractions": (
                "If ‘true’ interactions between the geneList’s first order interactors will be included. Ignored if includeInteractors is ‘false’ or if excludeGenes is set to ‘true’.",
                "Default=FALSE",
            ),
            "pubmedList": (
                "Interactions will be fetched whose Pubmed Id is/ is not in this list, depending on the value of excludePubmeds.",
                "Default=empty string",
            ),
            "excludePubmeds": (
                "If ‘false’, interactions with Pubmed ID in pubmedList will be included in the results; if ‘true’ they will be excluded.",
                "Default=FALSE",
            ),
            "htpThreshold": (
                "Interactions whose Pubmed ID has more than this number of interactions will be excluded from the results. Ignored if excludePubmeds is ‘false’.",
                "Default=2147483647 (maximum 32-bit integer)",
            ),
            "throughputTag": (
                "If set to 'low or 'high', only interactions with 'Low throughput' or 'High throughput' in the 'throughput' field will be returned. Interactions with both 'Low throughput' and 'High throughput' will be returned by either value.",
                "Default=“any”",
            ),
            "taxId": (
                "Only genes from these organisms will be searched with reference to gene identifiers or names.",
                "Default=“All”",
            ),
            "includeHeader": (
                "If ‘true’, the first line of the result will be a BioGRID column header, appropriate for the format parameter (‘count’ format has no header).",
                "Default=FALSE",
            ),
        }

    def __make_url(self, params):
        """Makes the API url for the queried params.
        """
        info = (("accessKey", self.key), ("format", "json"))
        params = self.__valid_keywords(params)
        params = tuple({(k, v) for k, v in params.items()})
        url = params + info
        encoded = urlencode(url, safe="|")
        endpoint = self.base_url + self.interactions + encoded
        return endpoint

    def get_interactions(self, **kwargs):
        """Fetches Protein-Protein interactions from BioGRID

        Args:
            Check the valid_keys attribute for a full list of arguments, with descriptions and defaults.
        
        Returns:
            A Pandas dataframe containing the protein-protein interactions.
        
        Raises:
            Exception: Couldn't retrieve interaction data from BioGRID, try again later or change your query.
        """
        endpoint = self.__make_url(kwargs)
        try:
            req = requests.get(endpoint).json()
        except:
            raise Exception(
                "Couldn't retrieve interaction data from BioGRID, try again later or change your query."
            )
        inter_table = pd.DataFrame(req).T.reset_index(drop=True)
        return inter_table

    def __valid_keywords(self, params):
        """Verifies that the arguments passed are valid and concatenatenates the geneList as specified by the API docs"""
        valid = list(self.valid_keys.keys())

        for param in params.keys():
            if param not in valid:
                raise ValueError(
                    f"{param} is not a valid argument, check the valid_keys attribute to see a list of them."
                )
            elif param == "geneList":
                # Checking the intersection
                if set(params.keys()) & set(valid[7:10]):
                    params[param] = "|".join(params[param])
                else:
                    raise ValueError(
                        f"If you pass a gene list, you have to pass one of these three arguments {valid[7:10]} as true, to indicate which ids you're using."
                    )

        return params
