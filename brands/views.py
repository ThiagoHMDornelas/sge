from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from . import models, forms


class BrandListView(ListView):
    model = models.Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class BrandCreateView(CreateView):
    model = models.Brand
    template_name = 'brand_create.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        # verifica qual botão foi clicado
        if "save_and_new" in self.request.POST:
            return HttpResponseRedirect(reverse("brand_create"))

        return response


class BrandDetailView(DetailView):
    model = models.Brand
    template_name = 'brand_detail.html'
    context_object_name = 'brand'


class BrandUpdateView(UpdateView):
    model = models.Brand
    template_name = 'brand_update.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')


class BrandDeleteView(DeleteView):
    model = models.Brand
    template_name = 'brand_delete.html'
    # form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')
