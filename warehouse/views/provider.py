from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from warehouse.forms import ProviderForm
from warehouse.models import Provider

class ProviderCreate(CreateView):
    model = Provider
    form_class = ProviderForm
    template_name = 'scrud/create.html'

    def get_success_url(self):
        return reverse('provider-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Criar Fornecedor"
        ctx['extra_js'] = ["js/django_apps/warehouse/provider/create.js"]

        return ctx

class ProviderUpdate(UpdateView):
    model = Provider
    form_class = ProviderForm
    template_name = 'scrud/create.html'

    def get_success_url(self):
        return reverse('provider-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Editar Fornecedor"
        ctx['extra_js'] = ["js/django_apps/warehouse/provider/create.js"]

        return ctx

class ProviderList(ListView):
    model = Provider
    context_object_name = 'object_list'
    fields = ['name', 'cnpj']
    template_name = 'scrud/list.html'

    options = {
        "Detalhar": {"btnClass": "info", "url": "provider-detail", "args": {'pk': ['id']}, "priority": True},
        "Editar": {"btnClass": "info", "url": "provider-update", "args": {'pk': ['id']}},
        "Deletar": {"btnClass": "danger", "url": "provider-delete", "args": {'pk': ['id']}},
    }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Listar Fornecedores"
        ctx['fields'] = self.fields
        ctx['urlOptions'] = self.options

        return ctx

class ProviderDetail(DetailView):
    model = Provider
    context_object_name = 'object'
    fields = ['name', 'cnpj', 'zip_code', 'address', 'neighborhood', 'city', 'state']
    template_name = 'scrud/detail.html'

    options = {
        'Deletar': {'btnClass': 'info', 'url': 'provider-delete', 'args': {'pk': ['id']}},
        'Editar': {'btnClass': 'info', 'url': 'provider-update', 'args': {'pk': ['id']}},
        'Voltar': {'btnClass': 'warning', 'url': 'provider-list', 'args': {}},
    }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Detalhes Fornecedor"
        ctx['fields'] = self.fields
        ctx['urlOptions'] = self.options
        ctx['extra_js'] = ["js/django_apps/warehouse/provider/detail.js"]

        return ctx

class ProviderDelete(DeleteView):
    model = Provider
    success_url = reverse_lazy('provider-list')
    template_name = 'scrud/delete.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.verbose_name = 'Deletar'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Deletar Fornecedor"

        return ctx
