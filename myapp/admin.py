from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import empresas, familias, articulos, perfil, tipomovimientos, clientes

admin.site.register(empresas)
admin.site.register(familias)
admin.site.register(articulos)
admin.site.register(perfil)
admin.site.register(Session)
admin.site.register(tipomovimientos)
admin.site.register(clientes)
# Register your models here.
