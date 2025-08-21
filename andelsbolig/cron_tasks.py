from fastapi import APIRouter, Depends, HTTPException
from pymongo import UpdateOne

from andelsbolig.advertisement.repository import AdvertisementRepository
from andelsbolig.agent.model import Agent
from andelsbolig.agent.repository import AgentRepository
from andelsbolig.agent.service import agent_advertisements
from andelsbolig.misc.logger import get_logger
from andelsbolig.notification.service import send_email
from andelsbolig.security.service import is_subscribed

logger = get_logger(__name__)
router = APIRouter()
agent_db = AgentRepository()
advertisement_db = AdvertisementRepository()


@router.post("/cron/check_agent_advertisement_matches", include_in_schema=False)
def check_agent_advertisement_matches():
    """For every active advertisement agent, check if the criteria matches any advertisements, and notify the users once."""
    mongo_operations = []
    agents = agent_db.read_many({"active": True}, Agent)

    for agent in agents:
        matched_advertisements = agent_advertisements(agent)
        for matched_advertisement in matched_advertisements:
            # Notify the user about the matched advertisement
            # An advertisement can have multiples emails
            for mail in matched_advertisement.emails:
                send_email(matched_advertisement, mail)

            update_operation = UpdateOne({"_id": matched_advertisement.id}, {"$push": {"notified_agents": agent.id}})
            mongo_operations.append(update_operation)

    if mongo_operations:
        logger.info(f"Adding agent ID to {len(mongo_operations)} advertisements")
        advertisement_db.bulk_write(mongo_operations)
