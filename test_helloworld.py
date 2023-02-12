import unittest
from flask import Flask
from flask_restful import Api
import app

class HelloWorldTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(app.HelloWorld, '/')
        self.client = self.app.test_client()

    def test_hello_world(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.get_json(), {'hello': 'world'})

if __name__ == '__main__':
    unittest.main()

