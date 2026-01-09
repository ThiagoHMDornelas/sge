from django import forms

from . import models


class ProductForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = ['name', 'category', 'brand', 'description', 'serie_number', 'cost_price', 'selling_price']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'serie_number': forms.TextInput(attrs={'class': 'form-control'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nome',
            'category': 'Categoria',
            'brand': 'Marca',
            'description': 'Descrição',
            'serie_number': 'Nro. Série',
            'cost_price': 'Preço de Custo',
            'selling_price': 'Preço de Venda',
        }
