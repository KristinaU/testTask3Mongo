# ***Reference: https://damyanon.net/post/flask-series-testing/***

# Unit tests cover the required functionality

import unittest
import models
from app import app

#client = app.test_client()


class MyTestClass(unittest.TestCase):

    # initialization logic for the test suite declared in the test module
    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(cls):
        pass

    # clean up logic for the test suite declared in the test module
    # code that is executed after all tests in one test run
    @classmethod
    def tearDownClass(cls):
        pass

    # initialization logic
    # code that is executed before each test
    def setUp(self):
        pass

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass

    # test method
    def test_equal_numbers(self):
        self.assertEqual(2, 2)

    # test registration
    def test_create_user(User):
        models.User.create_user('String1', 'String2') == 200

    # test create item
    def test_create_item(Item):
        models.Item.create_item(0, 'String1', 'String2') == 200

    # test registration POST
#    def test_registration_post(User):
#        response = client.post("/registration/")
#        response.status_code == 200

    # test users GET
#    def test_users_get(self):
#        response = client.get("/users/")
#        response.status_code == 200


# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()
