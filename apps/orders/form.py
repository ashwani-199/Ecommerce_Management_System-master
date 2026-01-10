from django import forms 
from apps.orders.models import Order, User

STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )


class OrderForm(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label = "Select a Customer",
        widget=forms.Select(
            attrs={'class': "form-control",}
        )
    )
    total_amount = forms.CharField(
        required=False, 
        label='Total Amount',
        widget=forms.TextInput(
            attrs={'class': "form-control ",
                   'placeholder': 'Total Amount'}),
        error_messages={
            'required': "The total amount field is required."
        }
    )
    status = forms.ChoiceField(choices=STATUS, widget=forms.Select(attrs={'class': "form-control"}))
    shipping_address = forms.CharField(
        required=False, 
        label='Shipping Address',
        widget=forms.TextInput(
            attrs={'class': "form-control",
                   'placeholder': 'Shipping Address'}),
        error_messages={
            'required': "The shipping address field is required."
        }
    )

    class Meta:
        model = Order
        fields = ['customer', 'total_amount', 'status', 'shipping_address']