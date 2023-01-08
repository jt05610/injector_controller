from unittest import IsolatedAsyncioTestCase

from fastapi import FastAPI
from httpx import AsyncClient
from uuid import uuid4

from modbus_device.config import MONGO_DB_CONN_STRING
from modbus_device.entrypoints.api.schema import map_routers
from motor.motor_asyncio import AsyncIOMotorClient


def random_ref():
    return f"ref-{uuid4()}"


class TestCRUD(IsolatedAsyncioTestCase):
    endpoint = "/device/data_model"

    async def asyncSetUp(self) -> None:
        self.db_client = AsyncIOMotorClient(MONGO_DB_CONN_STRING)
        self.app = FastAPI()
        self.app = map_routers(self.app, "fake", client=self.db_client)
        self.client = AsyncClient(app=self.app, base_url="http://test")

    def _id_endpoint(self, _id):
        return f"{self.endpoint}/{_id}"

    async def asyncTearDown(self) -> None:
        await self.client.delete("/device/data_model")
        await self.client.aclose()

    async def _insert_data_model(self):
        response = await self.client.post(
            self.endpoint,
            json={
                "ref": random_ref(),
                "discrete_inputs": ["btn_on"],
                "coils": ["collect", "calibrate"],
                "input_registers": ["reading"],
                "holding_registers": ["cal_slope", "cal_intercept"],
            },
        )
        return response

    async def _seed_db_(self, n_data_models):
        for _ in range(0, n_data_models):
            await self._insert_data_model()

    async def test_create(self):
        response = await self._insert_data_model()
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json().get("_id"))

    async def test_get_one(self):
        response = await self._insert_data_model()
        created = response.json()
        response = await self.client.get(f"{self.endpoint}/{created['_id']}")
        self.assertEqual(200, response.status_code)
        assert response.json() == created

    async def test_get_all(self):
        await self._seed_db_(20)
        response = await self.client.get(self.endpoint)
        self.assertEqual(200, response.status_code)
        self.assertEqual(20, len(response.json()))

    async def test_delete(self):
        await self._seed_db_(20)
        response = await self.client.delete("/device/data_model")
        self.assertEqual(200, response.status_code)
        response = await self.client.get(self.endpoint)
        self.assertEqual(0, len(response.json()))

    async def test_delete_one(self):
        response = await self._insert_data_model()
        _id = response.json().get("_id")
        response = await self.client.get(self.endpoint)
        self.assertEqual(1, len(response.json()))
        response = await self.client.delete(self._id_endpoint(_id))
        self.assertEqual(200, response.status_code)
        response = await self.client.get(self.endpoint)
        self.assertEqual(0, len(response.json()))

    async def test_update(self):
        expected = ["a", "b", "c", "d", "e"]
        response = await self._insert_data_model()
        created = response.json()
        _id = created.get("_id")
        response = await self.client.put(
            self._id_endpoint(_id), json={"coils": expected}
        )
        print(response.json())
        self.assertEqual(200, response.status_code)
        response = await self.client.get(self._id_endpoint(_id))
        self.assertEqual(expected, response.json().get("coils"))


class TestDevice(IsolatedAsyncioTestCase):
    endpoint = "/device"

    async def asyncSetUp(self) -> None:
        self.db_client = AsyncIOMotorClient(MONGO_DB_CONN_STRING)
        self.app = FastAPI()
        self.app, self.pub = map_routers(
            self.app, "fake", client=self.db_client, namespace="mockbus"
        )
        self.client = AsyncClient(app=self.app, base_url="http://test")

    def _id_endpoint(self, _id):
        return f"{self.endpoint}/{_id}"

    async def asyncTearDown(self) -> None:
        await self.pub.pubsub.close()
        await self.client.delete("/device")
        await self.client.aclose()

    async def _insert_data_model(self):
        response = await self.client.post(
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
        return response.json()

    async def _insert_device(self):
        dm = await (self._insert_data_model())
        response = await self.client.post(
            self.endpoint,
            json={
                "ref": f"fake_device",
                "node_address": 0xCC,
                "data_model_id": dm.get("_id"),
            },
        )
        assert response.status_code == 200
        return response.json()

    async def test_create(self):
        device = await self._insert_device()
        self.assertIsNotNone(device.get("_id"))

    async def test_get_one(self):
        created = await self._insert_device()
        response = await self.client.get(f"{self.endpoint}/{created['_id']}")
        self.assertEqual(200, response.status_code)

    async def test_update(self):
        created = await self._insert_device()
        data = {"node_address": 2}
        response = await self.client.put(f"{self.endpoint}/{created['_id']}", json=data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json().get("node_address"))

    async def test_get_all(self):
        for _ in range(0, 10):
            await self._insert_device()
        response = await self.client.get(f"{self.endpoint}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(10, len(response.json()))

    async def test_drop_one(self):
        for _ in range(0, 10):
            await self._insert_device()
        response = await self.client.get(f"{self.endpoint}")
        _id = response.json()[5].get("_id")
        await self.client.delete(f"{self.endpoint}/{_id}")
        response = await self.client.get(f"{self.endpoint}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(9, len(response.json()))

    async def test_drop_all(self):
        for _ in range(0, 10):
            await self._insert_device()
        response = await self.client.delete(f"{self.endpoint}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.json()))
    async def test_read(self):
        value = 0xFEEDBEEF
        device = await self._insert_device()
        _id = device.get("_id")
        self.pub.publish("mockbus.holding_registers.read.expect", value)
        response = await self.client.get(f"{self._id_endpoint(_id)}/cal_slope")
        self.assertEqual(200, response.status_code)
        await self.pub.publish()
        self.assertEqual({"value": value}, response.json())

    async def test_write(self):
        device = await self._insert_device()
        _id = device.get("_id")
        response = await self.client.post(
            f"{self._id_endpoint(_id)}/collect", json={"value": 1}
        )
        print(response.json())
        self.assertEqual(200, response.status_code)
        self.assertEqual({"ok": 1}, response.json())
