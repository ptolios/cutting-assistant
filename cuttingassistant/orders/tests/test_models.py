from django.test import TestCase
from django.utils import timezone

from orders.models import Order, OrderStatus

# return the values of the OrderStatus class properties
class_vars = [
    value for key, value in OrderStatus.__dict__.items()
    if not key.startswith('__')
]


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
        # placement_date for order1 is not provided
        # the default value is assigned, which is the datetime of creation
        now = timezone.now().replace(second=0, microsecond=0)
        self.assertAlmostEqual(self.order1.placement_datetime, now)

    def test_status(self):
        self.assertIn(self.order1.status, class_vars)

    def test_str(self):
        self.assertEqual(str(self.order1), f'Παραγγελία {self.order1.id}')


