from django.db import models

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    cnpj_vendor = models.CharField(max_length=20)
    city = models.CharField (null=True, blank=True,max_length=50)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'vendor'
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'


class Products(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'products'
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
