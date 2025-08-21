import unittest

from starlette.testclient import TestClient

from andelsbolig.config.properties import RUNNING_TESTS
from andelsbolig.security.service import create_jwt
from andelsbolig.user.repository import UserRepository
from tests.generator import generate_user_create
from .context import *

db = UserRepository()


# class TestSecurity(unittest.TestCase):
#
#     @classmethod
#     def tearDown(cls) -> None:
#         if RUNNING_TESTS:
#             db.delete_collection()
#
