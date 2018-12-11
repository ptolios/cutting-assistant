from django.test import TestCase
from django.urls import reverse

from orders.models import Order, OrderItem, OrderStatus


class TestOrdersView(TestCase):

    def test_orders_list_url(self):
        response = self.client.get("/orders/")
        self.assertEqual(response.status_code, 200)

    def test_orders_list_reverse_url(self):
        response = self.client.get(reverse("order_list"))
        self.assertEqual(response.status_code, 200)

    def test_views_use_correct_template(self):
        # Check the correct template of all the views here
        response = self.client.get(reverse("order_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order_list.html")


class TestOrderDetailsView(TestCase):
    
    def setUp(self):
        self.order1 = Order.objects.create(
            customer="John Papas",
            delivery_date="2018-05-02",
            status=OrderStatus.ACTIVE
        )
        self.orderitem1 = OrderItem.objects.create(
            order=self.order1,
            material="material #1",
            quantity=5,
            x_dimension=502.5,
            y_dimension=320
        )
        self.orderitem2 = OrderItem(
            order=self.order1,
            material="material #1",
            quantity=5,
            x_dimension=502.5,
            y_dimension=320
        )

    def test_order_details_url(self):
        response = self.client.get("/orders/1")
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("order_details", kwargs={"pk": "1"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order_details.html")

    def test_view_returns_correct_model_instance(self):
        response = self.client.get(reverse("order_details", kwargs={"pk": "1"}))
        response_order_id = response.context["order"].id
        self.assertEqual(self.order1.id, response_order_id)
