import json
from tests import TestBase


class TestAuth(TestBase):
    """ Test user registration and login """

    def test_registeration(self):
        """ Test user registration """
        self.user = {"username": "testuser2",
                     "password": "testpassword"}
        result = self.app.post("/api/v1.0/auth/register/",
                               data=self.user)
        self.assertEqual(result.status_code, 201)
        output = json.loads(result.data)
        self.assertTrue("You have successfully added a new user"
                        in output['Message'])

    def test_login(self):
        """ Test user login """
        self.user = {"username": "testuser",
                     "password": "testpassword"}
        result = self.app.post("/api/v1.0/auth/login/",
                               data=self.user)
        self.assertEqual(result.status_code, 200)
        output = json.loads(result.data)
        self.assertTrue("You have successfully logged in. "
                        "Use the token below to make requests"
                        in output['Message'])
