from django import forms

from .models import Order, OrderItem
from cuttingassistant.utils import now


class BaseModelForm(forms.ModelForm):
    # This class is used as a base to globally override 
    # the colon at the end of the labels

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BaseModelForm, self).__init__(*args, **kwargs)




class OrderForm(BaseModelForm):

    class Meta:
        model = Order
        exclude = (
            'status',
        )
        widgets = {
            'customer': forms.TextInput(
                attrs={
                    'class': 'white-text'
                }
            ),
            'placement_datetime': forms.DateTimeInput(
                attrs={
                    'class': 'white-text'
                }
            ),
            'delivery_date': forms.DateInput(
                format='%d/%m/%Y',
                attrs={
                    'class': 'white-text datepicker'
                }
            )
        }
        label_suffix = ''

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data.get('delivery_date')
        placement_datetime = self.cleaned_data.get('placement_datetime')
        if delivery_date:
            if placement_datetime.date() > delivery_date:
                raise forms.ValidationError(
                    'Η ημερομηνία παράδοσης δεν μπορεί να προηγείται της ημερομηνίας καταχώρισης',
                    code='invalid'
                )


class OrderItemForm(BaseModelForm):

    class Meta:
        model = OrderItem
        fields = ('quantity', 'x_dimension', 'y_dimension', 'material')
        labels = {
            'quantity': 'Τεμάχια',
            'x_dimension': 'Πλευρά 1',
            'y_dimension': 'Πλευρά 2',
        }
        widgets = {
            'quantity': forms.TextInput(),
            'x_dimension': forms.TextInput(),
            'y_dimension': forms.TextInput(),
            'material': forms.HiddenInput(),
        }


class MaterialForm(forms.Form):
    material = forms.CharField( label='Υλικό',
                                max_length=50,
                                widget=forms.TextInput(
                                            attrs={
                                                'class': 'white-text',
                                                'onblur': 'fillHiddenInput();',
                                            }
                                )
                              )


MaterialFormSet = forms.formset_factory(MaterialForm)


OrderItemFormset = forms.inlineformset_factory(
                            Order,
                            OrderItem,
                            form=OrderItemForm,
                            fields=(
                                'quantity',
                                'x_dimension',
                                'y_dimension',
                                'material'
                            ),
                            extra=1,
                            can_delete=False
                   )