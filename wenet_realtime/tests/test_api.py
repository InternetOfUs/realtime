import unittest

from fastapi.testclient import TestClient
from wenet_realtime.app import app
import json


class ClosestAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        user1 = {"id": "user1", "latitude": 0, "longitude": 0, "accuracy": 0}
        user2 = {"id": "user2", "latitude": 1, "longitude": 1, "accuracy": 0}
        user3 = {"id": "user3", "latitude": 9, "longitude": 9, "accuracy": 0}
        user4 = {"id": "user4", "latitude": 19, "longitude": 19, "accuracy": 0}
        for user in [user1, user2, user3, user4]:
            res = self.client.post("/users_locations/", json=user)

    def test_closest_first(self):
        params = {"latitude": 10, "longitude": 10}

        res = self.client.get("/closest/", params=params)
        first = list(res.json())[0]["userId"]
        self.assertEqual(first, "user3")

    def test_get_locations_one(self):
        res = self.client.post("/locations/", json={"userids": ["user1"]})
        items = res.json()
        first = items["locations"][0]
        self.assertEqual(first["latitude"], 0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
