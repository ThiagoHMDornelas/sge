from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from . import models, forms


class CategoryListView(ListView):
    model = models.Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class CategoryCreateView(CreateView):
    model = models.Category
    template_name = 'category_create.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        # verifica qual botão foi clicado
        if "save_and_new" in self.request.POST:
            return HttpResponseRedirect(reverse("category_create"))

        return response

    
class CategoryDetailView(DetailView):
    model = models.Category
    template_name = 'category_detail.html'
    context_object_name = 'category'


class CategoryUpdateView(UpdateView):
    model = models.Category
    template_name = 'category_update.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(DeleteView):
    model = models.Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('category_list')
