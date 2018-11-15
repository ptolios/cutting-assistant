from django.test import TestCase
from django.urls import reverse


class TestURLS(TestCase):

    def test_orders_list_url(self):
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 200)

    def test_orders_list_reverse_url(self):
        response = self.client.get(reverse('orders_list'))
        self.assertEqual(response.status_code, 200)
