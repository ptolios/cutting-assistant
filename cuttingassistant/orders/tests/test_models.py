from django.test import TestCase
from django.utils import timezone

from orders.models import Order, OrderItem, OrderStatus

# return the values of the OrderStatus class properties
class_vars = [
    value for key, value in OrderStatus.__dict__.items()
    if not key.startswith('__')
]


class TestOrderModel(TestCase):
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
        count_before: int = Order.objects.count()
        self.order2.save()
        count_after: int = Order.objects.count()
        self.assertEqual(count_after - count_before, 1)

    def test_placement_date(self):
        # placement_date for order1 is not provided
        # the default value is assigned, which is the datetime of creation
        now: "datetime" = timezone.now().replace(second=0, microsecond=0)
        self.assertAlmostEqual(self.order1.placement_datetime, now)

    def test_status(self):
        self.assertIn(self.order1.status, class_vars)

    def test_str(self):
        self.assertEqual(str(self.order1), f'Παραγγελία {self.order1.id}')


class TestOrderItemModel(TestCase):

    def setUp(self):
        self.order1 = Order.objects.create(
            customer='John Papas',
            delivery_date='2018-05-02',
            status=OrderStatus.ACTIVE
        )
        self.orderitem1 = OrderItem.objects.create(
            order=self.order1,
            quantity=5,
            x_dimension=502.5,
            y_dimension=320
        )
        self.orderitem2 = OrderItem(
            order=self.order1,
            quantity=25,
            x_dimension=178.2,
            y_dimension=255
        )

    def test_orderitem_saved(self):
        count_before: int = OrderItem.objects.count()
        self.orderitem2.save()
        count_after: int = OrderItem.objects.count()
        self.assertEqual(count_after - count_before, 1)

    def test_total_area(self):
        area1 = self.orderitem1.quantity * self.orderitem1.x_dimension * \
                     self.orderitem1.y_dimension / 1000000
        area2 = self.orderitem2.quantity * self.orderitem2.x_dimension * \
                     self.orderitem2.y_dimension / 1000000
        total_area1 = self.orderitem1.total_area()
        total_area2 = self.orderitem2.total_area()
        self.assertEqual(total_area1, area1)
        self.assertEqual(total_area2, area2)

    def test_str(self):
        self.assertEqual(
            str(self.orderitem1),
            f"Παραγγελία_{self.orderitem1.order.id} Στοιχείο Παραγγελίας_{self.orderitem1.id}"
        )
