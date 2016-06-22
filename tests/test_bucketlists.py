import json
from tests import TestBase


class TestBucketlists(TestBase):
    """ Test operations on bucket lists """

    def get_token(self):
        """ Returns authentication token """
        self.user = {"username": "testuser",
                     "password": "testpassword"}
        response = self.app.post("/api/v1.0/auth/login/",
                                 data=self.user)
        output = json.loads(response.data)
        token = output.get("token").encode("ascii")
        return {"token": token}

    def test_no_token(self):
        """ Test that users must provide a token to make responses """
        self.bucketlist = {"title": "24 Before 24",
                           "description": "24 things to do before I turn 24"}
        response = self.app.post("/api/v1.0/bucketlists/",
                                 data=self.bucketlist)
        self.assertEqual(response.status_code, 401)
        output = json.loads(response.data)
        self.assertTrue("Error: Please enter a token"
                        in output["message"])

    def test_invalid_token(self):
        """ Test that invalid tokens cannot be used """
        self.bucketlist = {"title": "24 Before 24",
                           "description": "24 things to do before I turn 24"}
        invalid_token = {"token": 12345}
        response = self.app.post("/bucketlists/",
                                 data=self.bucketlist,
                                 headers=invalid_token)
        self.assertEqual(response.status_code, 401)
        output = json.loads(response.data)
        self.assertTrue("Error: The token you have entered is invalid"
                        in output["message"])

    def test_add_bucketlist(self):
        """ Test addition of bucket lists """
        self.bucketlist = {"title": "24 Before 24",
                           "description": "24 things to do before I turn 24"}
        response = self.app.post("/api/v1.0/bucketlists/",
                                 data=self.bucketlist,
                                 headers=self.get_token())
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data)
        self.assertTrue("You have successfully added a new bucket list"
                        in output["message"])
        self.assertIn(self.bucketlist["title"], response.data)
        self.assertIn(self.bucketlist["description"], response.data)

    def test_delete_bucketlist(self):
        """ Test deletion of bucket lists """
        response = self.app.delete("/api/v1.0/bucketlists/1",
                                   headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertTrue("You have successfully deleted the following "
                        "bucket list" in output["message"])
        self.assertTrue("Knowledge Goals" in output["message"])

    def test_edit_bucketlist(self):
        """ Test editing of bucket lists """
        self.bucketlist = {"title": "Mission Multilinguist",
                           "description": "Languages to learn"}
        response = self.app.put("/api/v1.0/bucketlists/2",
                                data=self.bucketlist,
                                headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertTrue("You have successfully edited the bucket list"
                        in output["message"])
        self.assertIn(self.bucketlist["title"], response.data)
        self.assertIn(self.bucketlist["description"], response.data)

    def test_get_bucketlists(self):
        """ Test that all bucket lists are displayed """
        response = self.app.get("/api/v1.0/bucketlists/",
                                headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        output = output["bucketlists"]
        bucketlist1 = output[0]
        bucketlist2 = output[1]
        # Both bucket lists are displayed
        self.assertEqual(bucketlist1.get("title"), "Knowledge Goals")
        self.assertEqual(bucketlist2.get("title"), "Adventures")

    def test_get_bucketlist(self):
        """ Test that specified bucket list is displayed """
        # Get bucket list whose ID is 1
        response = self.app.get("/api/v1.0/bucketlists/1",
                                headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        bucketlist1 = json.loads(response.data)
        self.assertEqual(bucketlist1.get("title"), "Knowledge Goals")

        # Get bucket list whose ID is 2
        response = self.app.get("/api/v1.0/bucketlists/2",
                                headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        bucketlist1 = json.loads(response.data)
        self.assertEqual(bucketlist1.get("title"), "Adventures")

    def test_get_nonexistent_bucketlist(self):
        """
        Test that specifying a bucket list with invalid id
        will throw an error
        """
        response = self.app.get("/api/v1.0/bucketlists/200",
                                headers=self.get_token())
        self.assertEqual(response.status_code, 403)
        output = json.loads(response.data)
        self.assertTrue("The bucket list specified doesn't exist. "
                        "Please try again!" in output["message"])

    def test_unauthorized_access(self):
        """ Test that users cannot access another user's bucket lists """
        # Register a new user and obtain their token
        self.user = {"username": "testuser3",
                     "password": "testpassword"}
        response = self.app.post("/api/v1.0/auth/register/",
                                 data=self.user)
        response = self.app.post("/api/v1.0/auth/login/",
                                 data=self.user)
        output = json.loads(response.data)
        token = output.get("token").encode("ascii")
        token = {"token": token}

        # No bucket lists are displayed
        response = self.app.get("/api/v1.0/bucketlists/",
                                headers=token)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertTrue("You have no bucket lists. Add a new one and try again"
                        in output["message"])

        # Attempt to get another user's bucket list
        response = self.app.get("/api/v1.0/bucketlists/1",
                                headers=token)
        self.assertEqual(response.status_code, 403)
        output = json.loads(response.data)
        self.assertTrue("Error: You are not authorized to access this resource"
                        in output["message"])
