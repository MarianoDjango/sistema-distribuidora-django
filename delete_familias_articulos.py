import csv
import os
import django
import datetime
from decimal import Decimal
# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disilva.settings')
django.setup()

from myapp.models import articulos, familias

def delete_articulos():
    articulos_del = articulos.objects.all()
    for articulo in articulos_del:
        articulo.delete()
        print("Se borro el articulo : ", articulo)

def delete_familias():
    familias_del = familias.objects.all()
    for familia in familias_del:
        familia.delete()
        print("Se borro la familia : ", familia)

if __name__ == "__main__":
    delete_familias()
    delete_articulos()
