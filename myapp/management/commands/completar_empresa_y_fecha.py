# management/commands/completar_empresa.py
from django.core.management.base import BaseCommand
from django.db import transaction
from myapp.models import hist_movart, cabecera_venta

class Command(BaseCommand):
    help = 'Completa la empresa en hist_movart y cabecera_venta según el artículo'

    def handle(self, *args, **kwargs):
        movimientos = hist_movart.objects.select_related('articulo').all()
        cabeceras_dict = {}  # Para acumular cabeceras a actualizar
        hist_actualizar = []

        for m in movimientos:
            if not m.articulo or not m.articulo.idempresa:
                continue  # saltar movimientos sin artículo o sin empresa

            # Actualizar empresa en hist_movart
            m.empresa = m.articulo.idempresa
            hist_actualizar.append(m)

            # Si es venta, actualizar cabecera_venta
            if m.tipomov.lower() == 'venta':
                if m.numdoc not in cabeceras_dict:
                    cab = cabecera_venta.objects.filter(id=m.numdoc).first()
                    if cab:
                        cab.empresa = m.empresa
                        cabeceras_dict[m.numdoc] = cab

        # Guardar movimientos en batches
        batch_size = 500
        total_hist = 0
        for i in range(0, len(hist_actualizar), batch_size):
            hist_movart.objects.bulk_update(hist_actualizar[i:i+batch_size], ['empresa'])
            total_hist += len(hist_actualizar[i:i+batch_size])

        # Guardar cabeceras
        cabeceras_list = list(cabeceras_dict.values())
        cabecera_venta.objects.bulk_update(cabeceras_list, ['empresa'])

        # Informes
        self.stdout.write(self.style.SUCCESS(f'Movimientos hist_movart actualizados: {total_hist}'))
        self.stdout.write(self.style.SUCCESS(f'Cabeceras cabecera_venta actualizadas: {len(cabeceras_list)}'))
