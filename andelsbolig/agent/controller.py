import time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from andelsbolig.agent.model import Agent, AgentCreate
from andelsbolig.agent.repository import AgentRepository
from andelsbolig.misc.logger import get_logger
from andelsbolig.security.service import is_subscribed, is_authorized

router = APIRouter()
db = AgentRepository()
logger = get_logger(__name__)


@router.get("/agent/{_id}")
def get_agent(_id: str, _=Depends(is_subscribed)) -> dict:
    agent = db.read({"_id": _id})
    if agent is None:
        raise HTTPException(status_code=404, detail="Kunne ikke finde annonceagent")
    return agent


@router.get("/agent")
def get_agent(jwt=Depends(is_subscribed)) -> list[Agent]:
    # TODO Tror der er behov for et null check her
    agents = db.read_many({"created_by": jwt.sub}, Agent)
    return agents


@router.post("/agent")
def create_agent(agent_create: AgentCreate, jwt=Depends(is_subscribed)) -> Agent:
    agent = Agent(
        notifications=agent_create.notifications,
        active=agent_create.active,
        criteria=agent_create.criteria,
        created_by=jwt.sub,
        name=agent_create.name,
    )

    # User is only allowed to have 5 agents
    if db.col.count_documents({"created_by": jwt.sub}) >= 5:
        raise HTTPException(status_code=400, detail="Du kan kun have 5 annonce agenter")

    doc = Agent.model_dump(agent, by_alias=True)
    db.create(doc)
    return agent


@router.put("/agent")
def update_agent(agent: Agent, jwt=Depends(is_subscribed)):
    # Ensure the user is allowed to update the supplied agent
    is_authorized(jwt.sub, agent.created_by)

    # User is only allowed to have 5 agents
    if db.col.count_documents({"created_by": jwt.sub}) >= 5:
        raise HTTPException(status_code=400, detail="Du kan kun have 5 annonce agenter")

    agent.updated = int(time.time())
    doc = Agent.model_dump(agent, by_alias=True)
    db.replace({"_id": agent.id}, doc)


@router.delete("/agent/{_id}")
def delete_agent(_id, jwt=Depends(is_subscribed)):
    db.delete({"_id": _id, "created_by": jwt.sub})
