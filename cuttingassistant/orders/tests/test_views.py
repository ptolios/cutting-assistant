from django.test import TestCase
from django.urls import reverse


class TestOrdersViews(TestCase):

    def test_views_use_correct_template(self):
        # Check the correct template of all the views here
        response = self.client.get(reverse('orders_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order-list.html')
