from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from warehouse.forms import ProductForm
from warehouse.models import Product

class ProductCreate(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'scrud/create.html'

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Criar Produto"
        # ctx['extra_js'] = ["js/django_apps/condominium/create.js"]

        return ctx

class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'scrud/create.html'

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Editar Produto"
        # ctx['extra_js'] = ["js/django_apps/condominium/create.js"]

        return ctx

class ProductList(ListView):
    model = Product
    context_object_name = 'object_list'
    fields = ['description', 'price', 'quantity']
    template_name = 'scrud/list.html'

    options = {
        "Detalhar": {"btnClass": "info", "url": "product-detail", "args": {'pk': ['id']}, "priority": True},
        "Editar": {"btnClass": "info", "url": "product-update", "args": {'pk': ['id']}},
        "Deletar": {"btnClass": "danger", "url": "product-delete", "args": {'pk': ['id']}},
    }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Listar Produtos"
        ctx['fields'] = self.fields
        ctx['urlOptions'] = self.options

        return ctx

class ProductDetail(DetailView):
    model = Product
    context_object_name = 'object'
    fields = ['description', 'price', 'quantity']
    template_name = 'scrud/detail.html'

    options = {
        'Deletar': {'btnClass': 'info', 'url': 'product-delete', 'args': {'pk': ['id']}},
        'Editar': {'btnClass': 'info', 'url': 'product-update', 'args': {'pk': ['id']}},
        'Voltar': {'btnClass': 'warning', 'url': 'product-list', 'args' : {}},
    }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Detalhes Fornecedor"
        ctx['fields'] = self.fields
        ctx['urlOptions'] = self.options
        # ctx['extra_js'] = ["js/django_apps/condominium/detail.js"]

        return ctx

class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('provider-list')
    template_name = 'scrud/delete.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.verbose_name = 'Deletar'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = "Deletar Fornecedor"

        return ctx
