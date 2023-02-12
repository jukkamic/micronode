import unittest
import app

class CartTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app
        self.client = self.app.test_client()

    def test_get_empty_cart(self):
        response = self.client.get('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.get_json(), {'items': []})

    def test_post_to_cart(self):
        item = {'name': 'item1', 'price': 10}
        response = self.client.post('/cart', json=item)
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.get_json(), {'item': item})

        response = self.client.get('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.get_json(), {'items': [item]})

if __name__ == '__main__':
    unittest.main()
