import json
from tests import TestBase


class TestAuth(TestBase):
    """ Test user registration and login """

    def test_registeration(self):
        """ Test user registration """
        self.user = {"username": "testuser2",
                     "password": "testpassword"}
        request = self.app.post("/api/v1.0/auth/register/",
                                data=self.user)
        self.assertEqual(request.status_code, 201)
        output = json.loads(request.data)
        self.assertTrue("You have successfully added a new user"
                        in output["Message"])
        self.assertIn(self.user["username"], request.data)

    def test_login(self):
        """ Test user login """
        self.user = {"username": "testuser",
                     "password": "testpassword"}
        request = self.app.post("/api/v1.0/auth/login/",
                                data=self.user)
        self.assertEqual(request.status_code, 200)
        output = json.loads(request.data)
        self.assertTrue("You have successfully logged in"
                        in output["Message"])

    def test_invalid_credentials(self):
        """ Test that users cannot login with invalid credentials """
        self.user = {"username": "invalid",
                     "password": "testpassword"}
        request = self.app.post("/api/v1.0/auth/login/",
                                data=self.user)
        self.assertEqual(request.status_code, 403)
        output = json.loads(request.data)
        self.assertTrue("Error: Incorrect username and/or password."
                        in output["Message"])

        self.user = {"username": "testuser",
                     "password": "invalid"}
        request = self.app.post("/api/v1.0/auth/login/",
                                data=self.user)
        self.assertEqual(request.status_code, 403)
        output = json.loads(request.data)
        self.assertTrue("Error: Incorrect username and/or password."
                        in output["Message"])
