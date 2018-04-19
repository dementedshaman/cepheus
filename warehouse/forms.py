from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

from .models import Provider, Product, Entry, EntryItem
from localflavor.br.forms import BRCNPJField
import re

class ProviderForm(ModelForm):
    cnpj = BRCNPJField(min_length=16)

    def clean_cnpj(self):
        data = self.cleaned_data['cnpj']
        data = re.sub('[^0-9]','', data)
        return data

    class Meta:
        model = Provider
        fields = ['name', 'cnpj', 'zip_code', 'address', 'neighborhood', 'city', 'state']


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ['description', 'price', 'quantity']


class EntryForm(ModelForm):

    class Meta:
        model = Entry
        fields = ['entry_date', 'emission_date', 'register_date', 'provider', 'invoice', 'series', 'user']

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False # This is crucial.

        helper.layout = Layout(
            Fieldset('Criar Entrada', 'entry_date', 'emission_date', 'register_date', 'provider', 'invoice', 'series', 'user'),
        )

        return helper


class ItemFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.layout = Layout(
            Fieldset("Adicionar Item", 'product', 'quantity', 'base_price', 'discount', 'addition'),
        )


ItemFormset = inlineformset_factory(
    Entry,
    EntryItem,
    fields=['product', 'quantity', 'base_price', 'discount', 'addition',],
    extra=1,
    can_delete=False,
)

class EntryItemForm(ModelForm):

    class Meta:
        model = EntryItem
        fields = ['product', 'quantity', 'base_price', 'discount', 'addition', 'price']
