from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.db.models.functions import Lower

from . import models, forms


class BrandListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'
    paginate_by = 5
    permission_required = 'brands.view_brand'

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


class BrandCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Brand
    template_name = 'brand_create.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')
    permission_required = 'brands.add_brand'

    def form_valid(self, form):
        response = super().form_valid(form)

        # verifica qual botão foi clicado
        if "save_and_new" in self.request.POST:
            return HttpResponseRedirect(reverse("brand_create"))

        return response


class BrandDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Brand
    template_name = 'brand_detail.html'
    context_object_name = 'brand'
    permission_required = 'brands.view_brand'


class BrandUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Brand
    template_name = 'brand_update.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')
    permission_required = 'brands.change_brand'


class BrandDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Brand
    template_name = 'brand_delete.html'
    # form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')
    permission_required = 'brands.delete_brand'
