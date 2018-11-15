from django.urls import path
from django.views.generic import TemplateView

from .views import OrderListView

urlpatterns = [
    path('', OrderListView.as_view(), name='orders_list')
]