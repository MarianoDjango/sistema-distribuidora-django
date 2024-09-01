from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import empresas, familias, articulos, perfil, tipomovimientos, clientes, cabecera_venta, formaspago, hist_movart 

admin.site.register(empresas)
admin.site.register(familias)
admin.site.register(articulos)
admin.site.register(perfil)
admin.site.register(Session)
admin.site.register(tipomovimientos)
admin.site.register(clientes)
admin.site.register(cabecera_venta)
admin.site.register(formaspago)
admin.site.register(hist_movart)
# Register your models here.
