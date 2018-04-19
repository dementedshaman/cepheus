from django.db import models

# Create your models here.

class Provider(models.Model):
    name = models.CharField(verbose_name='Nome', max_length=100)
    cnpj = models.CharField(verbose_name='CNPJ', max_length=100)
    zip_code = models.CharField(verbose_name='CEP', max_length=100)
    address = models.CharField(verbose_name='Logradouro', max_length=100)
    neighborhood = models.CharField(verbose_name='Bairro', max_length=100)
    city = models.CharField(verbose_name='Cidade', max_length=100)
    state = models.CharField(verbose_name='Estado', max_length=100)

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'

    def __str__(self):
        return self.name


class Product(models.Model):
    description = models.CharField(verbose_name='Descrição', max_length=100)
    price = models.DecimalField(verbose_name='Preço', max_digits=10, decimal_places=2)
    quantity = models.IntegerField(verbose_name='Quantidade')

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.description


class Entry(models.Model):
    entry_date = models.DateTimeField(verbose_name='Data da Entrada')
    emission_date = models.DateTimeField(verbose_name='Data de Emissão')
    register_date = models.DateTimeField(verbose_name='Data de Registro')
    provider = models.ForeignKey('Provider', verbose_name='Fornecedor', on_delete=models.PROTECT, related_name='entry_provider')
    invoice = models.CharField(verbose_name='NumNota', max_length=100)
    series = models.CharField(verbose_name='Série', max_length=100)
    user = models.CharField(verbose_name='Usuário', max_length=100)

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return self.invoice


class EntryItem(models.Model):
    entry = models.ForeignKey('Entry', verbose_name='Entrada', on_delete=models.PROTECT, related_name='entryitem_entry')
    product = models.ForeignKey('Product', verbose_name='Produto', on_delete=models.PROTECT, related_name='eentryitem_product')
    quantity = models.IntegerField(verbose_name='Quantidade')
    base_price = models.DecimalField(verbose_name='Preço Base', max_digits=10, decimal_places=2)
    discount = models.DecimalField(verbose_name='Desconto', max_digits=10, decimal_places=2)
    addition = models.DecimalField(verbose_name='Acréscimo', max_digits=10, decimal_places=2)
    price = models.DecimalField(verbose_name='Preço', max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Item de Entrada'
        verbose_name_plural = 'Itens de Entrada'

    def __str__(self):
        return self.product
