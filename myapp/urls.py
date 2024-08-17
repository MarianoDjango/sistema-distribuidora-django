from django.urls import path, include
from . import views

urlpatterns = [
    path('afterlogin/', views.afterlogin, name='afterlogin'),
    path('dashboard/', views.dashboard_view.as_view(), name='dashboard'),
    path('articulos/', views.articulos_famila, name='articfam'),
    path('familias/', views.famlias_empresa, name='articfam'),
    path('dashboard/familias_por_empresa/<pk>/', views.famlias_empresa, name='famempresa'),
    path('dashboard/<pk>/articulos_por_familia/<id>/', views.articulos_por_familia, name='articulos_por_familia'),
]
