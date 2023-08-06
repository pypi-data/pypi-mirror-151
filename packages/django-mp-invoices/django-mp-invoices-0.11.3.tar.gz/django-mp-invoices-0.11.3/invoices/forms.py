
from datetime import datetime

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from djforms.fields import DatePickerField
from customers.models import Customer
from managers.models import Manager


class ReportForm(forms.Form):

    date_from = DatePickerField(label=_('Date from'), required=False)

    date_to = DatePickerField(label=_('Date to'), required=False)

    is_profit_included = forms.BooleanField(
        label=_('Include profit'),
        initial=False,
        required=False)

    is_wholesale_price_included = forms.BooleanField(
        label=_('Include wholesale price'),
        initial=False,
        required=False)

    is_discount_included = forms.BooleanField(
        label=_('Include discount'),
        initial=False,
        required=False)

    manager = forms.ModelChoiceField(
        empty_label=_('Select manager'),
        queryset=Manager.objects.all(),
        required=False)

    def __init__(self, data):

        today = datetime.now().date().strftime(settings.DATE_INPUT_FORMATS[0])

        super().__init__(
            data={
                'date_from': data.get('date_from', today),
                'date_to': data.get('date_to', today),
                'manager': data.get('manager'),
                'is_profit_included': data.get('is_profit_included'),
                'is_discount_included': data.get('is_discount_included'),
                'is_wholesale_price_included': data.get(
                    'is_wholesale_price_included')
            }
        )

        self.is_valid()


class ManageInvoiceForm(forms.Form):

    customer = forms.ModelChoiceField(
        empty_label=_('Select customer'),
        queryset=Customer.objects.all(),
        required=False)

    manager = forms.ModelChoiceField(
        empty_label=_('Select manager'),
        queryset=Manager.objects.all(),
        required=False)

    discount = forms.IntegerField(required=False)

    def __init__(self, invoice):

        super().__init__(
            initial={
                'customer': invoice.customer,
                'manager': invoice.manager,
                'discount': invoice.discount,
            }
        )

        self.fields['discount'].widget.attrs = {
            'data-role': 'discount-input',
            'class': 'invoice-discount-input',
            'data-url': invoice.update_url
        }
