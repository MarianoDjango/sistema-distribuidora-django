from django.urls import path, include
from . import views

urlpatterns = [
    path('afterlogin/', views.afterlogin, name='afterlogin'),
    path('dashboard/<id_empresa>/', views.dashboard_view.as_view(), name='dashboard'),
    path('articulos/', views.articulos_famila, name='articfam'),
    path('familias/', views.famlias_empresa, name='articfam'),
    path('articulo/<id_empresa>/<pk>/', views.articulo_create_or_update, name='article-detail'),
    path('actualizar_precios/', views.actualizar_precios, name='updateprices'),
    path('guardar_movimiento/', views.guardar_movs_stock, name='updatestocks'),
    path('dashboard/<id_empresa>/agregar/<int:articulo_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('dashboard/<id_empresa>/carrito/', views.ver_carrito, name='ver_carrito'),

]
