from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import empresas, familias, articulos

admin.site.register(empresas)
admin.site.register(familias)
admin.site.register(articulos)
admin.site.register(Session)

# Register your models here.
