from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from . import models


class TweetTest(APITestCase):
    PAYLOAD = "Tweet Test"

    def setUp(self):
        user = User.objects.create(username="testuser")
        user.set_password("password")
        user.save()

        self.client.force_login(user)

        models.Tweet.objects.create(
            user=user,
            payload=self.PAYLOAD
        )

    def test_tweet_create(self):
        response = self.client.post("/api/v1/tweets/", {
            "payload": self.PAYLOAD
        })
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["payload"], self.PAYLOAD)

    def test_tweet_list(self):
        response = self.client.get("/api/v1/tweets/")
        self.assertEqual(response.status_code, 200)

    def test_tweet_detail(self):
        response = self.client.get("/api/v1/tweets/2")
        self.assertEqual(response.status_code, 404)

        response = self.client.get("/api/v1/tweets/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["payload"], self.PAYLOAD)

    def test_tweet_update(self):
        response = self.client.put("/api/v1/tweets/2", {
            "payload": "Updated Tweet Test"
        })
        self.assertEqual(response.status_code, 404)

        response = self.client.put("/api/v1/tweets/1", {
            "payload": "Updated Tweet Test"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["payload"], "Updated Tweet Test")

    def test_tweet_delete(self):
        response = self.client.delete("/api/v1/tweets/1")
        self.assertEqual(response.status_code, 204)
