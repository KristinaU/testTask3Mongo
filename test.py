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

    # test Model create user username
    def test_model_create_user_username(self):
        new_user = models.User.create_user('String1', 'String2')
        self.assertEqual(new_user['username'], 'String1')


    # test Model create user password
    def test_model_create_user_password(self):
        new_user = models.User.create_user('String1', 'String2')
        self.assertEqual(new_user['password'], 'String2')


    # test Model create item id
    def test_create_item_id(self):
        new_item = models.Item.create_item(0, 'String1', 'String2')
        self.assertEqual(new_item['id'], 0)


    # test Model create item id
    def test_create_item_username(self):
        new_item = models.Item.create_item(1, 'String3', 'String3')
        self.assertEqual(new_item['username'], 'String3')


    # test Model create item id
    def test_create_item_item_name(self):
        new_item = models.Item.create_item(2, 'String4', 'String5')
        self.assertEqual(new_item['item_name'], 'String5')


    # test Model create item id
    def test_create_item_id(self):
        new_item = models.Item.create_item(0, 'String1', 'String2')
        self.assertEqual(new_item['id'], 0)

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
