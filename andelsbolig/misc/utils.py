""" Generelle utils der kan være til gavn alle steder i projektet """

import bson.regex

from logger import get_logger

logger = get_logger(__name__)


def create_filter(args):
    """Som udgangspunkt queries alt, hvortil brugeren kan supplere filters"""
    filter_ = {}

    logger.debug(f"Filter started as {filter_}")
    if "id" in args:
        filter_ |= {"_id": args["id"]}
    if "type" in args:
        filter_ |= {"type": args["type"]}
    if "text" in args and args["text"] != "null":
        regx = bson.regex.Regex(args["text"])
        filter_["$or"] = [
            {"name": {"$regex": regx, "$options": "i"}},
            {"description": {"$regex": regx, "$options": "i"}},
            {"pattern": {"$regex": regx, "$options": "i"}},
        ]
    return filter_


def get_query_params(
    type_,
):
    params = {
        # "page": page,
        # "size": size,
        "type": type_,
    }
    for param in list(params.keys()):
        if params[param] is None:
            del params[param]

    return params


class Singleton(type):
    """Utility class for creating Singleton classes"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
