import unittest
from unittest.mock import patch

from andelsbolig.advertisement.repository import AdvertisementRepository
from andelsbolig.agent.model import AgentCriteria
from andelsbolig.agent.repository import AgentRepository
from andelsbolig.config.properties import RUNNING_TESTS
from tests import client
from tests.generator import generate_advertisement_create, generate_agent_create

advertisement_db = AdvertisementRepository()
agent_db = AgentRepository()


def do_nothing(_, __):
    pass


class TestNotification(unittest.TestCase):

    @classmethod
    def tearDown(cls) -> None:
        if RUNNING_TESTS:
            advertisement_db.delete_collection()
            agent_db.delete_collection()

    @patch("andelsbolig.cron_tasks.send_email", new=do_nothing)
    def test_check_agent_advertisement_matches(self):
        """Create 1 advertisement & create agent to match, run cronjob, expect sent notification"""
        # Create advertisement
        advertisement_create = generate_advertisement_create()
        advertisement_create["price"] = 1_600_000
        advertisement_create["address"] = "Plantevej 31 3 th"
        advertisement_create["city"] = "Gentofte"
        advertisement_create["square_meters"] = 72
        r1 = client.post("/advertisement", json=advertisement_create)
        self.assertEqual(200, r1.status_code)

        # Create agent
        agent_create = generate_agent_create()
        agent_create.criteria = AgentCriteria(
            price_from=1_000_000, price_to=2_000_000, cities=["Gentofte"], square_meters_from=70, square_meters_to=200
        )

        r2 = client.post("/agent", json=agent_create.model_dump())
        self.assertEqual(200, r2.status_code)
        agent = r2.json()

        # Also create a dummy agent objects to ensure that the cronjob only sends notifications to the correct agent
        agent_create2 = generate_agent_create()
        agent_create2.criteria = AgentCriteria(cities=["Random"])
        r4 = client.post("/agent", json=agent_create2.model_dump())
        self.assertEqual(200, r4.status_code)

        # Run cronjob (twice to test it doesn't duplicate notifications)
        r5 = client.post("/cron/check_agent_advertisement_matches")
        r6 = client.post("/cron/check_agent_advertisement_matches")
        self.assertEqual(200, r5.status_code)
        self.assertEqual(200, r6.status_code)

        # Ensure notification was sent to the proper agent
        agent_was_notified = advertisement_db.exists({"notified_agents": agent["_id"]}, 1)
        self.assertTrue(agent_was_notified)
