from protlinks.biogrid import BioGrid
from pytest import raises
import os

bg = BioGrid(access_key=os.environ.get("ACCESS_KEY"))


def test_fake_arguments():
    with raises(ValueError) as exception:
        bg.get_interactions(i_am_fake="make me raise an error")


def test_no_id_spec():
    with raises(ValueError) as exception:
        bg.get_interactions(geneList=["MAPK10", "BRCA1"])


def test_minimal_example():
    bg.get_interactions(searchNames=True, geneList=["MAPK10", "BRCA1"])

