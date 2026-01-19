from django.contrib import admin
from django.urls import path, include
# from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #  path('logout/', admin.site.urls, name='logout'), #  LogoutView.as_view(next_page='login')

    path('', include('brands.urls')),
    path('', include('category.urls')),
    path('', include('supplier.urls')),
    path('', include('product.urls')),
    path('', include('inflow.urls')),
    path('', include('outflow.urls')),
    path('', views.home, name='home')
]
