from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.db.models.functions import Lower

from . import models, forms


class SupplierListView(ListView):
    model = models.Supplier
    template_name = 'supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()

        # filtro
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        # Ordenação
        order_by = self.request.GET.get('order_by', 'name')

        # Lista de campos permitidos para ordenação
        # Dicionário de ordenação com case-insensitive para campos de texto
        order_mapping = {
            'id': 'id',
            '-id': '-id',
            'name': Lower('name'),
            '-name': Lower('name').desc(),
            'description': Lower('description'),
            '-description': Lower('description').desc(),
        }

        if order_by in order_mapping:
            queryset = queryset.order_by(order_mapping[order_by])

        return queryset


class SupplierCreateView(CreateView):
    model = models.Supplier
    template_name = 'supplier_create.html'
    form_class = forms.SupplierForm
    success_url = reverse_lazy('supplier_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        # verifica qual botão foi clicado
        if "save_and_new" in self.request.POST:
            return HttpResponseRedirect(reverse("supplier_create"))

        return response


class SupplierDetailView(DetailView):
    model = models.Supplier
    template_name = 'supplier_detail.html'
    context_object_name = 'supplier'


class SupplierUpdateView(UpdateView):
    model = models.Supplier
    template_name = 'supplier_update.html'
    form_class = forms.SupplierForm
    success_url = reverse_lazy('supplier_list')


class SupplierDeleteView(DeleteView):
    model = models.Supplier
    template_name = 'supplier_delete.html'
    success_url = reverse_lazy('supplier_list')
