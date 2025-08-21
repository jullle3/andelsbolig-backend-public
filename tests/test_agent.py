import unittest

from andelsbolig.agent.repository import AgentRepository
from andelsbolig.config.properties import RUNNING_TESTS
from tests import client
from tests.generator import generate_agent_create

db = AgentRepository()


class TestAgent(unittest.TestCase):

    @classmethod
    def tearDown(cls) -> None:
        if RUNNING_TESTS:
            db.delete_collection()

    def test_agent_crud(self):
        # Create agent
        agent_create = generate_agent_create()
        r1 = client.post("/agent", json=agent_create.model_dump())
        self.assertEqual(200, r1.status_code)
        agent = r1.json()

        # Update agent
        agent["notifications"] = ["email"]
        r2 = client.put("/agent", json=agent)
        self.assertEqual(200, r2.status_code)

        # Read
        # Expect the notifications to be updated
        r3 = client.get(f"/agent", params={"_id": agent["_id"]})
        agents = r3.json()
        self.assertEqual("email", agents[0]["notifications"][0])

    def test_multiple_agents(self):
        agent_create1 = generate_agent_create()
        agent_create2 = generate_agent_create()

        r1 = client.post("/agent", json=agent_create1.model_dump())
        r2 = client.post("/agent", json=agent_create2.model_dump())
        self.assertEqual(200, r1.status_code)
        self.assertEqual(200, r2.status_code)

        agent1 = r1.json()
        agent2 = r2.json()

        r3 = client.get(f"/agent/{agent1['_id']}")
        r4 = client.get(f"/agent/{agent2['_id']}")

        self.assertEqual(200, r3.status_code)
        self.assertEqual(200, r4.status_code)
