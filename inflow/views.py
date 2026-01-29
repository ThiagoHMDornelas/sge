from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.db.models.functions import Lower

from . import models, forms, serializers


class InflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.InFlow
    template_name = 'inflow_list.html'
    context_object_name = 'inflows'
    paginate_by = 5
    permission_required = 'inflow.view_inflow'

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
            'supplier': Lower('supplier'),
            '-supplier': Lower('supplier').desc(),
            'quantity': Lower('quantity'),
            '-quantity': Lower('quantity').desc(),
            'created_at': 'created_at',
            '-created_at': '-created_at',
        }

        if order_by in order_mapping:
            queryset = queryset.order_by(order_mapping[order_by])

        return queryset


class InflowCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.InFlow
    template_name = 'inflow_create.html'
    form_class = forms.InflowForm
    success_url = reverse_lazy('inflow_list')
    permission_required = 'inflow.add_inflow'

    def form_valid(self, form):
        response = super().form_valid(form)

        # verifica qual botão foi clicado
        if "save_and_new" in self.request.POST:
            return HttpResponseRedirect(reverse("inflow_create"))

        return response


class InflowDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.InFlow
    template_name = 'inflow_detail.html'
    context_object_name = 'inflow'
    permission_required = 'inflow.view_inflow'


class InflowCreateListAPIView(generics.ListCreateAPIView):
    queryset = models.InFlow.objects.all()
    serializer_class = serializers.InflowSerializer


class InflowRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.InFlow.objects.all()
    serializer_class = serializers.InflowSerializer
