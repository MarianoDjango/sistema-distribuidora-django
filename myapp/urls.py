from django.urls import path, include
from . import views

urlpatterns = [
    path('afterlogin/', views.afterlogin, name='afterlogin'),
    path('dashboard/', views.dashboard_view.as_view(), name='dashboard'),
    path('articulos/', views.articulos_famila, name='articfam'),
    path('familias/', views.famlias_empresa, name='articfam'),
    path('articulo/<pk>/', views.articleView.as_view(), name='article-detail'),
]
