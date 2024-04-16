from django.test import TestCase
from django.urls import reverse
from .models import Product
from unittest.mock import patch, Mock
from requests.exceptions import RequestException


class StarbucksDataTestCase(TestCase):
    @patch('fetch_parse.views.requests.get')
    def test_get_starbucks_data(self, mock_get):
        mock_response = {
            'list': [
                {
                    'new_product': 'Y',
                    'product_name': 'Test Product',
                    'cate_name': 'Test Category',
                    'content': 'Test Content',
                    'kcal': 100,
                    'sugars': 20,
                    'protein': 5,
                    'caffeine': 50,
                    'sat_fat': 10,
                    'sodium': 15,
                    'imageUrl' : 'https://image.istarbucks.co.kr/upload/store/skuimg/2021/04/[9200000002487]_20210426091745609.jpg'
                }
            ]
        }

        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = mock_response

        url = reverse('get_starbucks_data', args=['product_name', 'Test Product'])
        mock_get.side_effect = RequestException()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 500)
        mock_get.assert_called_once_with('https://www.starbucks.co.kr/upload/json/menu/W0000171.js')

        mock_get.side_effect = None
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        product = Product.objects.first()
        self.assertTrue(product.new_product)
        self.assertEqual(product.product_name, 'Test Product')
        self.assertEqual(product.cate_name, 'Test Category')
        self.assertEqual(product.content, 'Test Content')
        self.assertEqual(product.calories, 100)
        self.assertEqual(product.sugars, 20)
        self.assertEqual(product.protein, 5)
        self.assertEqual(product.caffeine, 50)
        self.assertEqual(product.fat, 10)
        self.assertEqual(product.sodium, 15)
