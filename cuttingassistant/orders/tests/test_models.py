from django.test import TestCase
from django.utils import timezone

from .models import Order, OrderStatus


class TestModels(TestCase):
    def setUp(self):
        self.order1 = Order.objects.create(
            customer='John Papas',
            delivery_date='2018-05-02',
            status=OrderStatus.ACTIVE
        )
        self.order2 = Order(
            customer='Jane Doe',
            placement_datetime=timezone.now().replace(second=0, microsecond=0),
            delivery_date='2018-02-12',
            status=OrderStatus.DRAFT
        )

    def test_order_saved(self):
        count_before = Order.objects.count()
        self.order2.save()
        count_after = Order.objects.count()
        self.assertEqual(count_after - count_before, 1)

    def test_placement_date(self):
        now = timezone.now().replace(second=0, microsecond=0)
        self.assertEqual(self.order1.placement_datetime, now)

    def test_status(self):
        self.assertIn(self.order1.status, (1, 2, 3, 4, 5))

    def test_str(self):
        self.assertEqual(str(self.order1), f'Παραγγελία {self.order1.id}')


class TestURLS(TestCase):

    def test_orders_list_url(self):
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 200)

