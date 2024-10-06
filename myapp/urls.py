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
    path('dashboard/<id_empresa>/restar/<int:articulo_id>/', views.restar_al_carrito, name='restar_al_carrito'),
    path('dashboard/<id_empresa>/remove/<int:articulo_id>/', views.quitar_art_de_carrito, name='quitar_art_de_carrito'),
    path('dashboard/<id_empresa>/cantidad/', views.cantidad_total_carrito, name='cantidad_total_carrito'),
    path('dashboard/<id_empresa>/carrito/', views.ver_carrito, name='ver_carrito'),
    path('dashboard/<id_empresa>/clientes/', views.clientes_view.as_view(), name='clientes'),
    path('dashboard/<id_empresa>/clientes/<pk>/', views.cliente_create_or_update, name='cliente'),
    path('clientes/', views.clientes_empresa, name='clientesempresa'),
    path('dashboard/<id_empresa>/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('dashboard/<id_empresa>/carrito/finalizar_compra/', views.cerrar_venta, name='cerrar_venta'),
    path('dashboard/<id_empresa>/movimientos/', views.movimientos_list_view, name='movimientos_list'),
    path('ajax/list-movimientos/', views.ajax_list_movimientos, name='ajax_list_movimientos'),
]
