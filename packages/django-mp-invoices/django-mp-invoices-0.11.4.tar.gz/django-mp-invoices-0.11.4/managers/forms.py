
from django import forms
from django.utils.translation import ugettext_lazy as _

from managers.models import Manager


class ManagerSelectForm(forms.Form):

    manager = forms.ModelChoiceField(
        empty_label=_('Select manager'),
        queryset= Manager.objects.all(),
        required=False)
