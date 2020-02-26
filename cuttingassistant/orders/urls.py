from django.urls import path
from django.views.generic import TemplateView

from .views import OrderCreateView, OrderDetailsView, OrderListView

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('<int:pk>', OrderDetailsView.as_view(), name='order_details'),
    path('new', OrderCreateView.as_view(), name='order_new'),
]
