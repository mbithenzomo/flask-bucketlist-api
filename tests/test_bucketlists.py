import json
from tests import TestBase


class TestBucketlists(TestBase):
    """ Test operations on bucket lists """

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
        self.bucketlist = {"title": "24 Before 24",
                           "description": "24 things to do before I turn 24"}
        request = self.app.post("/api/v1.0/bucketlists/",
                                data=self.bucketlist)
        self.assertEqual(request.status_code, 403)
        output = json.loads(request.data)
        self.assertTrue("Error: Please enter a token"
                        in output["Message"])

    def test_invalid_token(self):
        """ Test that invalid tokens cannot be used """
        self.bucketlist = {"title": "24 Before 24",
                           "description": "24 things to do before I turn 24"}
        invalid_token = {"Token": 12345}
        request = self.app.post("/bucketlists/",
                                data=self.bucketlist,
                                headers=invalid_token)
        self.assertEqual(request.status_code, 403)
        output = json.loads(request.data)
        self.assertTrue("Error: The token you have entered is invalid"
                        in output["Message"])

    def test_add_bucketlist(self):
        """ Test addition of bucket lists """
        self.bucketlist = {"title": "24 Before 24",
                           "description": "24 things to do before I turn 24"}
        request = self.app.post("/api/v1.0/bucketlists/",
                                data=self.bucketlist,
                                headers=self.get_token())
        self.assertEqual(request.status_code, 201)
        output = json.loads(request.data)
        self.assertTrue("You have successfully added a new bucket list"
                        in output["Message"])
        self.assertIn(self.bucketlist["title"], request.data)
        self.assertIn(self.bucketlist["description"], request.data)

    def test_delete_bucketlist(self):
        """ Test deletion of bucket lists """
        request = self.app.delete("/api/v1.0/bucketlists/1",
                                  headers=self.get_token())
        self.assertEqual(request.status_code, 200)
        output = json.loads(request.data)
        self.assertTrue("You have successfully deleted the following "
                        "bucket list" in output["Message"])

    def test_edit_bucketlist(self):
        """ Test editing of bucket lists """
        self.bucketlist = {"title": "Mission Multilinguist",
                           "description": "Languages to learn"}
        request = self.app.put("/api/v1.0/bucketlists/2",
                               data=self.bucketlist,
                               headers=self.get_token())
        self.assertEqual(request.status_code, 201)
        output = json.loads(request.data)
        self.assertTrue("You have successfully edited the bucket list"
                        in output["Message"])
        self.assertIn(self.bucketlist["title"], request.data)
        self.assertIn(self.bucketlist["description"], request.data)

    def test_get_bucketlists(self):
        """ Test that bucket lists are displayed """
        request = self.app.get("/api/v1.0/bucketlists/",
                               headers=self.get_token())
        self.assertEqual(request.status_code, 201)
        bucketlist1 = json.loads(request.data)[0]
        bucketlist2 = json.loads(request.data)[1]
        # Both bucket lists are displayed
        self.assertEqual(bucketlist1.get("title"), "Knowledge Goals")
        self.assertEqual(bucketlist2.get("title"), "Adventures")

    def test_get_bucketlist(self):
        """ Test that specified bucket list is displayed """
        # Get bucket list whose ID is 1
        request = self.app.get("/api/v1.0/bucketlists/1",
                               headers=self.get_token())
        self.assertEqual(request.status_code, 201)
        bucketlist1 = json.loads(request.data)
        self.assertEqual(bucketlist1.get("title"), "Knowledge Goals")

        # Get bucket list whose ID is 2
        request = self.app.get("/api/v1.0/bucketlists/2",
                               headers=self.get_token())
        self.assertEqual(request.status_code, 201)
        bucketlist1 = json.loads(request.data)
        self.assertEqual(bucketlist1.get("title"), "Adventures")
