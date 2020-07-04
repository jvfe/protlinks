import pandas as pd
from utils import get_string_info

## Using the API might work better, very much a WIP

class StringDB-API:
    def __init__(self):
        pass

    def make_sublists(self, genes):

        if len(genes) >= 2000:
            sublisted = [genes[i : i + 2000] for i in range(0, len(genes), 2000)]
            return sublisted

        else:
            return genes

    def get_interaction(self):
        pass