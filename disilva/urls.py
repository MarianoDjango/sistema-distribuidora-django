from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('myapp/', include('myapp.urls')),  # Ruta para la aplicación interna
    path('', views.index, name='landingindex'),
]
