from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.db.models.functions import Lower

from . import models, forms


class OutflowListView(ListView):
    model = models.OutFlow
    template_name = 'outflow_list.html'
    context_object_name = 'outflows'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        # filtro
        product = self.request.GET.get('product')
        if product:
            queryset = queryset.filter(product__name__icontains=product)

        # Ordenação
        order_by = self.request.GET.get('order_by', '-created_at')

        # Lista de campos permitidos para ordenação
        # Dicionário de ordenação com case-insensitive para campos de texto
        order_mapping = {
            'id': 'id',
            '-id': '-id',
            'product': Lower('product'),
            '-product': Lower('product').desc(),
            'quantity': Lower('quantity'),
            '-quantity': Lower('quantity').desc(),
            'created_at': 'created_at',
            '-created_at': '-created_at',
        }

        if order_by in order_mapping:
            queryset = queryset.order_by(order_mapping[order_by])

        return queryset


class OutflowCreateView(CreateView):
    model = models.OutFlow
    template_name = 'outflow_create.html'
    form_class = forms.OutflowForm
    success_url = reverse_lazy('outflow_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        # verifica qual botão foi clicado
        if "save_and_new" in self.request.POST:
            return HttpResponseRedirect(reverse("outflow_create"))

        return response


class OutflowDetailView(DetailView):
    model = models.OutFlow
    template_name = 'outflow_detail.html'
    context_object_name = 'outflow'
