from andelsbolig.advertisement.model import Advertisement
from andelsbolig.advertisement.repository import AdvertisementRepository
from andelsbolig.agent.model import Agent
from andelsbolig.config.properties import EARTH_RADIUS_KM
from andelsbolig.geo.geo import postal_dict

advertisement_db = AdvertisementRepository()


def agent_advertisements(agent: Agent) -> list[Advertisement]:
    """Find relevant advertisements for a given agent"""
    query = construct_mongo_query(agent)
    return advertisement_db.read_many(query, Advertisement)


def construct_mongo_query(agent: Agent) -> dict:
    """
    Constructs a MongoDB query based on the agent's criteria.
    :param agent: The agent whose criteria are used to build the query.
    :return: A dictionary representing the MongoDB query.
    """
    # Advertisements must be created after the agent, since we assume users are not interested in or have already analyzed old advertisements
    query = {"created": {"$gte": agent.created}}
    # Advertisement must not have already been notified to the agent
    query |= {"notified_agents": {"$nin": [agent.id]}}
    # Advertisement must be visible and not deleted
    query |= {"deleted": False, "visible": True}

    criteria = agent.criteria
    # Price
    if criteria.price_to is not None or criteria.price_from is not None:
        query["price"] = {}
        if criteria.price_from:
            query["price"] |= {"$gte": criteria.price_from}
        if criteria.price_to:
            query["price"] |= {"$lte": criteria.price_to}

    # Rooms
    if criteria.rooms_from is not None or criteria.rooms_to is not None:
        query["rooms"] = {}
        if criteria.rooms_from:
            query["rooms"] |= {"$gte": criteria.rooms_from}
        if criteria.rooms_to:
            query["rooms"] |= {"$lte": criteria.rooms_to}

    # Square meters
    if criteria.square_meters_from is not None or criteria.square_meters_to is not None:
        query["square_meters"] = {}
        if criteria.square_meters_from:
            query["square_meters"] |= {"$gte": criteria.square_meters_from}
        if criteria.square_meters_to:
            query["square_meters"] |= {"$lte": criteria.square_meters_to}

    # Cities criteria
    if criteria.cities:
        query |= {"city": {"$in": criteria.cities}}

    if criteria.radius is not None and criteria.postal_numbers:
        postal_number = criteria.postal_numbers[0]
        if postal_number in postal_dict:
            postal_record = postal_dict[postal_number]
            # 1. Convert the radius from kilometers to radians
            radius_in_radians = criteria.radius / EARTH_RADIUS_KM

            # 2. Build the $geoWithin + $centerSphere query
            query |= {
                "location": {
                    "$geoWithin": {"$centerSphere": [[postal_record.long, postal_record.lat], radius_in_radians]}
                }
            }

    return query
