import pandas as pd
import tempfile
import requests
import json
from tqdm import tqdm


def down_db(url, filename):
    dirpath = tempfile.mkdtemp()
    chunk_size = 1024

    db = requests.get(url, stream=True)

    if db.status_code != 200:
        raise Exception(
            "Couldn't find the database, did you give the right NCBI tax id?"
        )

    total_size = int(db.headers["content-length"])

    curr_total = total_size / chunk_size

    path = f"{dirpath}/{filename}"

    # https://www.thepythoncode.com/article/download-files-python

    progress = tqdm(
        db.iter_content(chunk_size),
        "Downloading database",
        total=curr_total,
        unit="KB",
        unit_scale=True,
        unit_divisor=1024,
    )

    with open(path, "wb") as f:
        for data in progress:
            f.write(data)
            progress.update(len(data))

    return path


def make_stringdb_url(info_type, version, species):
    """
  Return download url for stringdb, info_type being links or info (aliases).
  """

    url = f"https://stringdb-static.org/download/protein.{info_type}.v{version}/{species}.protein.{info_type}.v{version}.txt.gz"
    return url


def get_string_info(species):

    r = requests.get("https://string-db.org/api/json/version")
    version = r.json()[0]["string_version"]

    url = make_stringdb_url("links", version, species)

    return url, version


def get_string_aliases(version, species):
    url = make_stringdb_url("info", version, species)
    dirpath = tempfile.mkdtemp()
    db = requests.get(url)
    path = f"{dirpath}/{species}-pt_info.txt.gz"

    with open(path, "wb") as f:
        f.write(db.content)

    pt_info = pd.read_table(path, sep="\t")[["protein_external_id", "preferred_name"]]
    return pt_info
