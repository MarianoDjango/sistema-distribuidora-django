import csv
import os
import django

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disilva.settings')
django.setup()

from myapp.models import articulos

def importar_articulos(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(f"El artículo {row} ya existe en la base de datos.")

if __name__ == "__main__":
    csv_file = 'dsilva/articulos.csv'
    importar_articulos(csv_file)
