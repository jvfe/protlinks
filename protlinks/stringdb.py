import pandas as pd
from utils import down_db, get_string_aliases, get_string_info


class StringDB:
    def __init__(self, species):

        self.species = species
        url, self.version = get_string_info(species)
        self.data = down_db(url, f"{species}.txt.gz")
        self.aliases = get_string_aliases(self.version, species)

    def __merge_info(self, data):

        merged = pd.merge(
            data,
            self.aliases,
            right_on=["protein_external_id"],
            left_on=["protein1"],
            how="left",
        ).drop(columns=["protein_external_id"])

        return merged

    def get_neighbors(self, genes, min_score=600):

        interacts = pd.read_table(self.data, sep=" ")
        data = self.__merge_info(interacts)

        interest = data[data["preferred_name"].isin(genes)]
        if interest.empty:
            example = data["preferred_name"].iloc[0]
            raise ValueError(
                f"Couldnt find any interactions! Are the genes in the right format? Genes should look like {example}"
            )

        interest = interest.query("combined_score >= @min_score")
        if interest.empty:
            raise ValueError("Couldn't find any interactions for the required score!")

        return interest.drop(columns=["preferred_name"])

    def __repr__(self):
        return f"<StringDB(v{self.version}) network data for species {self.species}>"


rhiz = StringDB(species="1500304")

genes = ["JQKY01000021_gene2060", "Y01000003_gene347", "JQKY01000004_gene1432"]

rhiz.get_neighbors(genes, min_score=800)

