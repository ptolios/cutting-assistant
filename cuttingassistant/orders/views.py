from django.http import HttpResponseRedirect, HttpResponse
from django.forms.formsets import all_valid
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView

from cuttingassistant.utils import now, forms_are_valid
from .models import Order, OrderStatus
from .forms import MaterialForm, OrderForm, OrderItemFormset


class OrderListView(ListView):
    model = Order
    context_object_name = 'order_list'
    template_name = 'order_list.html'


class OrderDetailsView(DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'order_details.html'


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items_formset'] = OrderItemFormset(
                                            self.request.POST or None
                                        )
        context['material_form'] = MaterialForm(
                                        self.request.POST or None, 
                                        # auto_id=False,
                                        label_suffix=''
                                    )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_items_formset = context['order_items_formset']
        material_form = context['material_form']

        # if forms_are_valid(form, order_items_formset, material_form):
        if all_valid([form, order_items_formset, material_form]):

            order = form.save(commit=False)
            # self.object.placement_datetime = now()
            order.status = OrderStatus.ACTIVE
            order.save()
            # order_items_formset.instance = self.object
            order_items = order_items_formset.save(commit=False)
            for order_item in order_items:
                order_item.order = order
                order_item.save()

            return super().form_valid(form)
        else:
            # return HttpResponse('<h2>The forms are not valid!</h2>')
            return render(self.request, self.template_name, context=context)
