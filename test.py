# ***Reference: https://damyanon.net/post/flask-series-testing/***


import unittest
import models

# Warning: these tests are testing Models behaviour only
# actual API functionality was tested with Postman application


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
        print('Test 1 ok')
        self.assertEqual(2, 2)

    # test Model create user username
    def test_model_create_user_username(self):
        new_user = models.User.create_user('String1', 'String2')
        print('Test 2 OK' + new_user['username'])
        self.assertEqual(new_user['username'], 'String1')

    # test Model create user password
    def test_model_create_user_password(self):
        new_user = models.User.create_user('String1', 'String2')
        print('Test 3 OK' + new_user['password'])
        self.assertEqual(new_user['password'], 'String2')

    # test Model create item id
    def test_create_item_id(self):
        new_item = models.Item.create_item(0, 'String1', 'String2')
        print('Test 4 OK', new_item['id'])
        self.assertEqual(new_item['id'], 0)

    # test Model create item username
    def test_create_item_username(self):
        new_item = models.Item.create_item(1, 'String3', 'String3')
        print('Test 5 OK' + new_item['username'])
        self.assertEqual(new_item['username'], 'String3')

    # test Model create item item_name
    def test_create_item_item_name(self):
        new_item = models.Item.create_item(2, 'String4', 'String5')
        print('Test 6 OK' + new_item['item_name'])
        self.assertEqual(new_item['item_name'], 'String5')


# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()
