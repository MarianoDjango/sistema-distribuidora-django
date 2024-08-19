import csv
import os
import django
import datetime
from decimal import Decimal
# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disilva.settings')
django.setup()

from myapp.models import empresas, articulos, familias

def importar_articulos(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        empresa_var = 0
        familia_var = 0
        for row in reader:
            try:
                art = articulos.objects.get(idempresa=row['idempresa'], familia=row['idfamilia'], descripcion=row['descripcion'])
                print("articulo ya existe: ", art)
            except articulos.DoesNotExist:
                if familia_var != row['idfamilia']:
                    idempresa = empresas.objects.get(id=row['idempresa'])
                    family = familias.objects.get(id=row["idfamilia"])
                    familia_var = family.id

                descripcion = row["descripcion"].strip()
                try:
                    precio_venta = Decimal(row["precio publico"].strip())
                except:
                    precio_venta = 0

                fecha_precio = datetime.datetime.strptime(row["fecha precio"].strip(), "%d-%m-%Y").date() if row["fecha precio"] != "0" else datetime.datetime.today()
                try:
                    stock = Decimal(row["stock"].strip())
                except:
                    stock = 0
                fecha_stock = datetime.datetime.strptime(row["fecha stock"].strip(), "%d-%m-%Y").date() if row["fecha stock"] != "0" else datetime.datetime.today()
                activo = True if row["activo"] == "TRUE" else False
                comentarios = row["comentarios"]
                
                articulo = articulos(idempresa=idempresa, 
                                     familia=family, 
                                     descripcion=descripcion, 
                                     precio_venta=precio_venta,
                                     fecha_precio=fecha_precio,
                                     stock=stock,
                                     fecha_stock=fecha_stock,
                                     activo=activo,
                                     comentarios=comentarios
                                     )
                try:
                    articulo.save()
                    print("se creo el articulo : ", articulo.descripcion)
                except Exception as error:
                    print(error)

def importar_familias(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        empresa_var = 0
        for row in reader:
            try:
                fam = familias.objects.get(idempresa=row['idempresa'], nombre=row["nombre"])
                print("La familia ya existe: ", fam)
            except familias.DoesNotExist:
                if empresa_var != row['idempresa']:
                    idempresa = empresas.objects.get(id=row['idempresa'])
                    empresa_var = idempresa.id
                familia = familias(idempresa=idempresa, nombre=row["nombre"])
                familia.save()
                print("se creo la familia : ", familia.nombre)

if __name__ == "__main__":
    csv_file = 'familias.csv'
    importar_familias(csv_file)
    csv_file = 'articulos.csv'
    importar_articulos(csv_file)
