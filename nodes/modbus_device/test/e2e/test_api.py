import unittest
from unittest import IsolatedAsyncioTestCase

from fastapi import FastAPI

from fastapi.testclient import TestClient
import motor.motor_asyncio
from uuid import uuid4
from modbus_device.entrypoints.api.api import app, MONGO_DB_CONN_STRING

from modbus_device.entrypoints.api.schema import map_routers


def random_ref():
    return f"ref-{uuid4()}"


class TestDevice(unittest.TestCase):
    client: TestClient
    db_client: motor.motor_asyncio.AsyncIOMotorClient
    app: FastAPI()

    def setUp(self) -> None:
        self.app = FastAPI()
        self.db_client = MongoDB(
            MONGO_DB_CONN_STRING
        )
        map_routers(self.app, self.db_client, "fake")
        self.client = TestClient(self.app)

    def tearDown(self) -> None:
        self.db_client.drop_database("fake")

    def test_create(self):
        response = self.client.post(
                "/device/data_model",
                json={
                    "ref": random_ref(),
                    "discrete_inputs": ["btn_on"],
                    "coils": ["collect", "calibrate"],
                    "input_registers": ["reading"],
                    "holding_registers": ["cal_slope", "cal_intercept"],
                },
            )
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json().get("_id"))

    def test_list(self):
        for i in range(0, 5):
            self.client.post(
                "/device/data_model",
                json={
                    "ref": random_ref(),
                    "discrete_inputs": ["btn_on"],
                    "coils": ["collect", "calibrate"],
                    "input_registers": ["reading"],
                    "holding_registers": ["cal_slope", "cal_intercept"],
                },
            )
        response = self.client.get("/device/data_model/")
        print(response.json())
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json().get("_id"))

    async def test_get_one(self):
        pass
