from django.views.generic import DetailView, ListView

from .models import Order


class OrderListView(ListView):
    model = Order
    context_object_name = 'order_list'
    template_name = 'order_list.html'


class OrderDetailsView(DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'order_details.html'
