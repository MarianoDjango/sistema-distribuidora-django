from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='landingindex'),
    path('nosotros/', views.nosotros, name='landingnosotros'),
    path('myapp/', include('myapp.urls')),  # Ruta para la aplicación interna
]
