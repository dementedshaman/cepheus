from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.http import HttpResponseRedirect

from warehouse.forms import EntryForm, ItemFormset, ItemFormHelper
from warehouse.models import EntryItem, Entry

class EntryCreate(CreateView):
    form_class = EntryForm
    template_name = 'scrud/createBom.html'
    model = Entry

    def get_success_url(self):
        return reverse('entry-detail', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        item_form = ItemFormset()
        item_formhelper = ItemFormHelper()

        return self.render_to_response(
            self.get_context_data(form=form, item_form=item_form)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        item_form = ItemFormset(self.request.POST)

        if (form.is_valid() and item_form.is_valid()):
            return self.form_valid(form, item_form)

        return self.form_invalid(form, item_form)

    def form_valid(self, form, item_form):
        """
        Called if all forms are valid. Creates a Entry instance along
        with associated items and then redirects to a success page.
        """
        self.object = form.save()
        item_form.instance = self.object
        items = item_form.save()
        for item in items:
            item.price = (item.base_price * (1 - (item.discount/100)) * (1 + (item.addition/100))) * item.quantity
            item.save()
            product = item.product
            product.price = item.price
            product.quantity += item.quantity
            product.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, item_form):
        """
        Called if whether a form is invalid. Re-renders the context
        data with the data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, item_form=item_form)
        )

    def get_context_data(self, **kwargs):
        """ Add formset and formhelper to the context_data. """
        ctx = super().get_context_data(**kwargs)
        item_formhelper = ItemFormHelper()

        if self.request.POST:
            ctx['form'] = EntryForm(self.request.POST)
            ctx['item_form'] = ItemFormset(self.request.POST)
            ctx['item_formhelper'] = item_formhelper
        else:
            ctx['form'] = EntryForm()
            ctx['item_form'] = ItemFormset()
            ctx['item_formhelper'] = item_formhelper

        ctx['title'] = "Oi"
        ctx['extra_js'] = ["js/django_apps/warehouse/entry/create.js"]
        return ctx

class EntryList(ListView):
    model = Entry
    context_object_name = 'object_list'
    fields = ['provider', 'invoice']
    template_name = 'scrud/list.html'

    options = {
        "Detalhar": {"btnClass": "info", "url": "entry-detail", "args": {'pk': ['id']}, "priority": True},
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Lista de Entradas"
        context['fields'] = self.fields
        context['urlOptions'] = self.options

        return context

class EntryDetail(DetailView):
    model = Entry
    context_object_name = 'object'
    fields = ['provider', 'invoice', 'entry_date', 'emission_date', 'register_date', 'series', 'user']
    template_name = 'scrud/detail.html'

    options = {
        'Deletar': {'btnClass': 'info', 'url': 'entry-delete', 'args': {'pk': ['id']}},
        'CSV': {'btnClass': 'info', 'url': 'entry-csv', 'args': {'pk': ['id']}},
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Detalhes Entrada"
        context['fields'] = self.fields
        context['extra_js'] = ["js/django_apps/condominium/detail.js"]
        context['urlOptions'] = self.options

        extra_tables = {
            'itens': {
                'list': self.object.entryitem_entry,
                'fields': ['product', 'quantity', 'base_price', 'discount', 'addition', 'price'],
                'count': len(self.object.entryitem_entry.all()),
                'options': {}
            },
        }

        context['extra_tables'] = extra_tables
        return context

class EntryDelete(DeleteView):
    model = Entry
    success_url = reverse_lazy('entry-list')
    template_name = 'scrud/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Deletar Entrada"

        return context

import csv
from django.http import HttpResponse

def some_view(request, pk):
    ent = Entry.objects.get(pk=pk)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    fields = ['product', 'quantity', 'base_price', 'discount', 'addition', 'price']
    writer = csv.writer(response)
    writer.writerow(fields)
    for ei in ent.entryitem_entry.all():
        writer.writerow([getattr(ei, field) for field in fields])

    return response
