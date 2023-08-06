
from django import forms
from django.utils.translation import ugettext_lazy as _

from customers.models import Customer


class CustomerSelectForm(forms.Form):

    customer = forms.ModelChoiceField(
        empty_label=_('Select customer'),
        queryset=Customer.objects.all(),
        required=False)


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
