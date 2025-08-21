import csv
from collections import namedtuple

from definitions import ROOT_DIR

PostalRecord = namedtuple("PostalRecord", ["nr", "navn", "long", "lat"])


def load_postal_numbers_in_memory():
    """
    Reads the postal data CSV and returns a dictionary keyed by postalCode (nr),
    with the value as a PostalRecord namedtuple.
    """
    in_memory_postals = {}

    with open(ROOT_DIR + "/data/postal_data", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            nr = int(row["nr"])
            record = PostalRecord(
                nr=nr,
                navn=row["navn"],
                long=float(row["visueltcenter_x"]),
                lat=float(row["visueltcenter_y"]),
            )
            in_memory_postals[nr] = record

    return in_memory_postals


postal_dict = load_postal_numbers_in_memory()
