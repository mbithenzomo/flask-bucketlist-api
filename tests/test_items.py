import json
from tests import TestBase


class TestItems(TestBase):
    """ Test operations on bucket list items """

    def get_token(self):
        """ Returns authentication token """
        self.user = {"username": "testuser",
                     "password": "testpassword"}
        request = self.app.post("/api/v1.0/auth/login/",
                                data=self.user)
        output = json.loads(request.data)
        token = output.get("Token").encode("ascii")
        return {"Token": token}

    def test_no_token(self):
        """ Test that users must provide a token to make requests """
        self.item = {"title": "Learn to dive",
                     "description": "Dive from 20 metres"}
        request = self.app.post("/api/v1.0/bucketlists/2/items/",
                                data=self.item)
        self.assertEqual(request.status_code, 403)
        output = json.loads(request.data)
        self.assertTrue("Error: Please enter a token"
                        in output["Message"])

    def test_invalid_token(self):
        """ Test that invalid tokens cannot be used """
        self.item = {"title": "Learn to dive",
                     "description": "Dive from 20 metres"}
        invalid_token = {"Token": 12345}
        request = self.app.post("/api/v1.0/bucketlists/2/items/",
                                data=self.item,
                                headers=invalid_token)
        self.assertEqual(request.status_code, 403)
        output = json.loads(request.data)
        self.assertTrue("Error: The token you have entered is invalid"
                        in output["Message"])

    def test_add_item(self):
        """ Test addition of bucket list items """
        self.item = {"title": "Learn to dive",
                     "description": "Dive from 20 metres"}
        request = self.app.post("/api/v1.0/bucketlists/2/items/",
                                data=self.item,
                                headers=self.get_token())
        self.assertEqual(request.status_code, 201)
        output = json.loads(request.data)
        self.assertTrue("You have successfully added a new bucket list item"
                        in output["Message"])
        self.assertIn(self.item["title"], request.data)
        self.assertIn(self.item["description"], request.data)

    def test_delete_item(self):
        """ Test deletion of bucket list items """
        request = self.app.delete("/api/v1.0/bucketlists/1/items/1",
                                  headers=self.get_token())
        self.assertEqual(request.status_code, 200)
        output = json.loads(request.data)
        self.assertTrue("You have successfully deleted the following "
                        "bucket list" in output["Message"])
        self.assertTrue("Learn to Cook" in output["Message"])

    def test_edit_item(self):
        """ Test editing of bucket list items """
        self.item = {"title": "Play Piano",
                     "description": "Learn to play at least 5 songs by heart"}
        request = self.app.put("/api/v1.0/bucketlists/1/items/1",
                               data=self.item,
                               headers=self.get_token())
        self.assertEqual(request.status_code, 201)
        output = json.loads(request.data)
        self.assertTrue("You have successfully edited the bucket list item"
                        in output["Message"])
        self.assertIn(self.item["title"], request.data)
        self.assertIn(self.item["description"], request.data)

    def test_get_items(self):
        """ Test that all bucket list items are displayed """
        self.item = {"title": "Play Piano",
                     "description": "Learn to play at least 5 songs by heart"}
        self.app.post("/api/v1.0/bucketlists/1/items/",
                      data=self.item,
                      headers=self.get_token())
        request = self.app.get("/api/v1.0/bucketlists/1/items/",
                               headers=self.get_token())
        self.assertEqual(request.status_code, 201)
        bucketlist1 = json.loads(request.data)[0]
        bucketlist2 = json.loads(request.data)[1]
        # Both bucket list items are displayed
        self.assertEqual(bucketlist1.get("title"), "Learn to Cook")
        self.assertEqual(bucketlist2.get("title"), "Play Piano")

    def test_get_item(self):
        """ Test that specified bucket list item is displayed """
        # Get bucket list item whose ID is 1, and bucket list ID is 1
        request = self.app.get("/api/v1.0/bucketlists/1/items/1",
                               headers=self.get_token())
        self.assertEqual(request.status_code, 201)
        bucketlist1 = json.loads(request.data)
        self.assertEqual(bucketlist1.get("title"), "Learn to Cook")

        # Get bucket list item whose ID is 2, and bucket list ID is 2
        request = self.app.get("/api/v1.0/bucketlists/2/items/2",
                               headers=self.get_token())
        self.assertEqual(request.status_code, 201)
        bucketlist1 = json.loads(request.data)
        self.assertEqual(bucketlist1.get("title"), "Swim with Dolphins")

    def test_get_nonexistent_item(self):
        """
        Test that specifying a bucket list item with invalid id
        will throw an error
        """
        request = self.app.get("/api/v1.0/bucketlists/1/items/200",
                               headers=self.get_token())
        self.assertEqual(request.status_code, 403)
        output = json.loads(request.data)
        self.assertTrue("The bucket list item specified does not exist. "
                        "Please try again!" in output["Message"])

    def test_unauthorized_access(self):
        """ Test that users cannot access another user's bucket list items """
        # Register a new user and obtain their token
        self.user = {"username": "testuser3",
                     "password": "testpassword"}
        request = self.app.post("/api/v1.0/auth/register/",
                                data=self.user)
        request = self.app.post("/api/v1.0/auth/login/",
                                data=self.user)
        output = json.loads(request.data)
        token = output.get("Token").encode("ascii")
        token = {"Token": token}

        # Attempt to get another user's bucket list item
        request = self.app.get("/api/v1.0/bucketlists/1/items/1",
                               headers=token)
        self.assertEqual(request.status_code, 403)
        output = json.loads(request.data)
        self.assertTrue("Error: You are not authorized to access this resource"
                        in output["Message"])
