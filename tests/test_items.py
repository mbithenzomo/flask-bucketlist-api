import json
from tests import TestBase


class TestItems(TestBase):
    """ Test operations on bucket list items """

    def get_token(self):
        """ Returns authentication token """
        self.user = {"username": "testuser",
                     "password": "testpassword"}
        response = self.app.post("/api/v1/auth/login/",
                                 data=self.user)
        output = json.loads(response.data)
        token = output.get("token").encode("ascii")
        return {"token": token}

    def test_no_token(self):
        """ Test that users must provide a token to make responses """
        self.item = {"title": "Learn to dive",
                     "description": "Dive from 20 metres"}
        response = self.app.post("/api/v1/bucketlists/2/items/",
                                 data=self.item)
        self.assertEqual(response.status_code, 401)
        output = json.loads(response.data)
        self.assertTrue("Error: Please enter a token"
                        in output["message"])

    def test_invalid_token(self):
        """ Test that invalid tokens cannot be used """
        self.item = {"title": "Learn to dive",
                     "description": "Dive from 20 metres"}
        invalid_token = {"token": 12345}
        response = self.app.post("/api/v1/bucketlists/2/items/",
                                 data=self.item,
                                 headers=invalid_token)
        self.assertEqual(response.status_code, 401)
        output = json.loads(response.data)
        self.assertTrue("Error: The token you have entered is invalid"
                        in output["message"])

    def test_add_item(self):
        """ Test addition of bucket list items """
        self.item = {"title": "Learn to dive",
                     "description": "Dive from 20 metres"}
        response = self.app.post("/api/v1/bucketlists/2/items/",
                                 data=self.item,
                                 headers=self.get_token())
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data)
        self.assertTrue("You have successfully added a new bucket list item"
                        in output["message"])
        self.assertIn(self.item["title"], response.data)
        self.assertIn(self.item["description"], response.data)

    def test_delete_item(self):
        """ Test deletion of bucket list items """
        response = self.app.delete("/api/v1/bucketlists/1/items/1",
                                   headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertTrue("You have successfully deleted the following "
                        "bucket list" in output["message"])
        self.assertTrue("Learn to Cook" in output["message"])

    def test_edit_item(self):
        """ Test editing of bucket list items """
        self.item = {"title": "Play Piano",
                     "description": "Learn to play at least 5 songs by heart"}
        response = self.app.put("/api/v1/bucketlists/1/items/1",
                                data=self.item,
                                headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertTrue("You have successfully edited the bucket list item"
                        in output["message"])
        self.assertIn(self.item["title"], response.data)
        self.assertIn(self.item["description"], response.data)

    def test_get_items(self):
        """ Test that all bucket list items are displayed """
        self.item = {"title": "Play Piano",
                     "description": "Learn to play at least 5 songs by heart"}
        self.app.post("/api/v1/bucketlists/1/items/",
                      data=self.item,
                      headers=self.get_token())
        response = self.app.get("/api/v1/bucketlists/1/items/",
                                headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        bucketlist1 = json.loads(response.data)[0]
        bucketlist2 = json.loads(response.data)[1]
        # Both bucket list items are displayed
        self.assertEqual(bucketlist1.get("title"), "Learn to Cook")
        self.assertEqual(bucketlist2.get("title"), "Play Piano")

    def test_get_item(self):
        """ Test that specified bucket list item is displayed """
        # Get bucket list item whose ID is 1, and bucket list ID is 1
        response = self.app.get("/api/v1/bucketlists/1/items/1",
                                headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        bucketlist1 = json.loads(response.data)
        self.assertEqual(bucketlist1.get("title"), "Learn to Cook")

        # Get bucket list item whose ID is 2, and bucket list ID is 2
        response = self.app.get("/api/v1/bucketlists/2/items/2",
                                headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        bucketlist1 = json.loads(response.data)
        self.assertEqual(bucketlist1.get("title"), "Swim with Dolphins")

    def test_get_nonexistent_item(self):
        """
        Test that specifying a bucket list item with invalid id
        will throw an error
        """
        response = self.app.get("/api/v1/bucketlists/1/items/200",
                                headers=self.get_token())
        self.assertEqual(response.status_code, 403)
        output = json.loads(response.data)
        self.assertTrue("The bucket list item specified does not exist. "
                        "Please try again!" in output["message"])

    def test_unauthorized_access(self):
        """ Test that users cannot access another user's bucket list items """
        # Register a new user and obtain their token
        self.user = {"username": "testuser3",
                     "password": "testpassword"}
        response = self.app.post("/api/v1/auth/register/",
                                 data=self.user)
        response = self.app.post("/api/v1/auth/login/",
                                 data=self.user)
        output = json.loads(response.data)
        token = output.get("token").encode("ascii")
        token = {"token": token}

        # Attempt to get another user's bucket list item
        response = self.app.get("/api/v1/bucketlists/1/items/1",
                                headers=token)
        self.assertEqual(response.status_code, 403)
        output = json.loads(response.data)
        self.assertTrue("Error: You are not authorized to access this resource"
                        in output["message"])
