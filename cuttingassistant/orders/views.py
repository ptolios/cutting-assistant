from django.views.generic import ListView

from .models import Order


class OrderListView(ListView):
    model = Order
    context_object_name = 'order_list'
    template_name = 'order-list.html'
