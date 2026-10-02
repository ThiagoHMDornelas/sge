from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views
from authentication.views import profile

handler404 = views.custom_404

urlpatterns = [
    path('admin/', admin.site.urls),

    # *** DOCS ***
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password/change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('profile/', profile, name='profile'),

    path('api/v1/', include('authentication.urls')),

    path('', views.home, name='home'),
    path('', include('brands.urls')),
    path('', include('category.urls')),
    path('', include('supplier.urls')),
    path('', include('product.urls')),
    path('', include('inflow.urls')),
    path('', include('outflow.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
