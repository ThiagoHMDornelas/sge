from django.contrib import admin
from django.urls import path, include
# from django.contrib.auth import views as auth_views
# from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('brands.urls')),
    path('', include('category.urls'))
]
