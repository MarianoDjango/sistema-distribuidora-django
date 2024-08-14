from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/<pk>/', views.dashboard_view, name='dashboard'),
    path('dashboard/familias_por_empresa/<pk>/', views.familias_por_empresa, name='famempresa'),
]
