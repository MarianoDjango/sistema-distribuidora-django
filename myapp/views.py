from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import empresas, familias, articulos, hist_movart, tipomovimientos
import json
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .forms import articulosForm
import datetime
from decimal import Decimal
from django.urls import reverse
def index(request):
    return render(request, 'index.html')

def afterlogin( request, *args, **kwargs):
    idempresa = request.user.perfil.idempresa
    urlredirect = "/myapp/dashboard/" + str(idempresa.id)
    return redirect(urlredirect)

def famlias_empresa(request, **kwargs):
    empresa_id = request.GET['idempresa']
    familias_var = familias.objects.filter(idempresa=empresa_id)
    id_familia = familias_var[0].id if familias_var else None
    recs = []
    for fam in familias_var:
        fila = f'<a id="fam{fam.id}" href="javascript:void(0);" class="list-group-item border-end-0 d-inline-block text-truncate" data-bs-parent="#sidebar" onclick="ponerfamilia({fam.id}, \'{fam.nombre}\')"><span>{fam.nombre}</span></a>'
        recs.append({'fila': fila})
    
    data = {'filas' : recs,
            'id_familia' : id_familia}
    return JsonResponse(data)

def articulos_famila(request, **kwargs):
    recs = []
    json_list = {}
    if request.user.is_authenticated:
        familia_id = request.GET['familia']
        nombre_var = request.GET['nombre']
        idempresa_var = request.GET['idempresa']
        if nombre_var == "":
            articles = articulos.objects.filter(familia=int(familia_id), activo=True).values('id', 'idempresa','descripcion', 'precio_venta', 'fecha_precio', 'stock', 'fecha_stock', 'familia', 'precio_compra' )
        else:
            articles = articulos.objects.filter(familia=int(familia_id), descripcion__icontains=nombre_var, activo=True).values('id', 'idempresa','descripcion', 'precio_venta', 'fecha_precio', 'stock', 'fecha_stock', 'precio_compra')
        familia = familias.objects.get(id=int(familia_id))
        recs.append(json_list)
        for articulo in articles:
            fila = '<tr style="cursor:hand;">'
            if articulo['idempresa'] == request.user.perfil.idempresa.id or request.user.is_staff:
                id_articulo = str(articulo['id'])
                fila += f'<td class="text-center"><div class="form-check"><input class="form-check-input" type="checkbox" value="" id="flexCheckDefault{id_articulo}"><label class="form-check-label" for="flexCheckDefault{id_articulo}"></label></div></td>'
                fila += '<td><a href="../../articulo/' + idempresa_var + '/' + str(articulo['id']) + '/" id="descri' + str(articulo['id']) + '">' + articulo['descripcion'] + '</a></td>'
                fila += '<td class="text-end">' + '{:,.2f}'.format(articulo['precio_venta']).replace(",", "@").replace(".", ",").replace("@", ".") + '</td>'
                fila += '<td class="text-center">' + str(articulo['fecha_precio'].strftime('%d-%b-%Y').lower()) + '</td>'
                fila += '<td class="text-end">' +  '{:,.2f}'.format(articulo['stock']).replace(",", "@").replace(".", ",").replace("@", ".") + '</button></td>'
                fila += '<td class="text-center">' + str(articulo['fecha_stock'].strftime('%d-%b-%Y').lower()) + '</td>'
                fila += f'<td class="text-center"><input type="text" class="form-control" style="border-radius: 10px;" placeholder="Cant."></td>'
                fila += f'<td class="text-center"><button class="btn agregar-carrito" data-id="'+ str(articulo['id']) + '" style="background-color: #92dea3;" title="Agregar al Pedido"><i class="bi bi-cart-plus"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cart-plus" viewBox="0 0 16 16"><path d="M9 5.5a.5.5 0 0 0-1 0V7H6.5a.5.5 0 0 0 0 1H8v1.5a.5.5 0 0 0 1 0V8h1.5a.5.5 0 0 0 0-1H9z"/><path d="M.5 1a.5.5 0 0 0 0 1h1.11l.401 1.607 1.498 7.985A.5.5 0 0 0 4 12h1a2 2 0 1 0 0 4 2 2 0 0 0 0-4h7a2 2 0 1 0 0 4 2 2 0 0 0 0-4h1a.5.5 0 0 0 .491-.408l1.5-8A.5.5 0 0 0 14.5 3H2.89l-.405-1.621A.5.5 0 0 0 2 1zm3.915 10L3.102 4h10.796l-1.313 7zM6 14a1 1 0 1 1-2 0 1 1 0 0 1 2 0m7 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0"/></svg></i></button></td>'
                fila += f'<td class="text-end"><button class="btn btn-success entrada-stock" title="Entrada Stock" data-id-articulo="' +  id_articulo + '" data-toggle="modal" data-target="#movimientoStockModal"><i class="bi bi-window-plus"></i><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-window-plus" viewBox="0 0 16 16"><path d="M2.5 5a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1M4 5a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1m2-.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0"/><path d="M0 4a2 2 0 0 1 2-2h11a2 2 0 0 1 2 2v4a.5.5 0 0 1-1 0V7H1v5a1 1 0 0 0 1 1h5.5a.5.5 0 0 1 0 1H2a2 2 0 0 1-2-2zm1 2h13V4a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1z"/><path d="M16 12.5a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0m-3.5-2a.5.5 0 0 0-.5.5v1h-1a.5.5 0 0 0 0 1h1v1a.5.5 0 0 0 1 0v-1h1a.5.5 0 0 0 0-1h-1v-1a.5.5 0 0 0-.5-.5"/></svg></i></button></td>'
                fila += f'<td class="text-end"><button class="btn btn-danger salida-stock" title="Salida Stock" data-id-articulo="' +  id_articulo + '" data-toggle="modal" data-target="#movimientoStockModal"><i class="bi bi-window-dash"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-window-dash" viewBox="0 0 16 16"><path d="M2.5 5a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1M4 5a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1m2-.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0"/><path d="M0 4a2 2 0 0 1 2-2h11a2 2 0 0 1 2 2v4a.5.5 0 0 1-1 0V7H1v5a1 1 0 0 0 1 1h5.5a.5.5 0 0 1 0 1H2a2 2 0 0 1-2-2zm1 2h13V4a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1z"/><path d="M16 12.5a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0m-5.5 0a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 0-1h-3a.5.5 0 0 0-.5.5"/></svg></i></button></td>'
                fila += f'<td class="text-end"><button class="btn btn-secondary actualizar-stock" title="Regularizar Stock" data-id-articulo="' +  id_articulo + '" data-toggle="modal" data-target="#movimientoStockModal"><i class="bi bi-boxes"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-boxes" viewBox="0 0 16 16"><path d="M7.752.066a.5.5 0 0 1 .496 0l3.75 2.143a.5.5 0 0 1 .252.434v3.995l3.498 2A.5.5 0 0 1 16 9.07v4.286a.5.5 0 0 1-.252.434l-3.75 2.143a.5.5 0 0 1-.496 0l-3.502-2-3.502 2.001a.5.5 0 0 1-.496 0l-3.75-2.143A.5.5 0 0 1 0 13.357V9.071a.5.5 0 0 1 .252-.434L3.75 6.638V2.643a.5.5 0 0 1 .252-.434zM4.25 7.504 1.508 9.071l2.742 1.567 2.742-1.567zM7.5 9.933l-2.75 1.571v3.134l2.75-1.571zm1 3.134 2.75 1.571v-3.134L8.5 9.933zm.508-3.996 2.742 1.567 2.742-1.567-2.742-1.567zm2.242-2.433V3.504L8.5 5.076V8.21zM7.5 8.21V5.076L4.75 3.504v3.134zM5.258 2.643 8 4.21l2.742-1.567L8 1.076zM15 9.933l-2.75 1.571v3.134L15 13.067zM3.75 14.638v-3.134L1 9.933v3.134z"/></svg></i></button></td>'
                fila += '<td class="text-center preciocompra" style="display : none;">' + '{:,.2f}'.format(articulo['precio_compra']).replace(",", "@").replace(".", ",").replace("@", ".") + '</td>'
            else:
                fila += '<td>'+ articulo['descripcion'] + '</td>'
                fila += '<td class="text-end">{:,.2f}'.format(articulo['precio_venta']).replace(",", "@").replace(".", ",").replace("@", ".") + '</td>'
                fila += '<td class="text-center">' + str(articulo['fecha_precio']) + '</td>'
                fila += '<td class="text-end">{:,.2f}'.format(articulo['stock']).replace(",", "@").replace(".", ",").replace("@", ".") + '</td>'
                fila += '<td class="text-center">' + str(articulo['fecha_stock']) + '</td>'
            fila += '<td class="text-center" style="display : none;">' + str(articulo['id']) + '</td>'
            json_list = {
                'fila': fila,
            }
            recs.append(json_list)
    
    data = json.dumps(recs)
    return HttpResponse(data, 'application/json')

class dashboard_view(LoginRequiredMixin,View):
    template_name = 'myapp/dashboard.html'
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        empresa_id = kwargs['id_empresa']
        empresa_obj = get_object_or_404(empresas, id=empresa_id)
        companies_var = empresas.objects.all()  # Obtenemos todas las empresas
        empresa_user = self.request.user.perfil.idempresa.id
        nomempresa_user = self.request.user.perfil.idempresa.name
        familias_var = familias.objects.filter(idempresa=empresa_id)
        familia = familias_var[0]
        motivos_entrada = tipomovimientos.objects.filter(tipo='entrada')
        motivos_salida = tipomovimientos.objects.filter(tipo='salida').exclude(motivo='venta')
        motivos_regularizacion = tipomovimientos.objects.filter(tipo='regularizacion')

        context = {'empresas': companies_var,
                    'id_empresa':int(empresa_id),
                    'nomempresa' : empresa_obj.name, 
                    'id_familia' : familia.id,
                    'familia_nom' : familia.nombre,
                    'motivos_entrada': motivos_entrada,
                    'motivos_salida': motivos_salida,
                    'motivos_regularizacion': motivos_regularizacion
        }

        return render(self.request, self.template_name, context)

@login_required
def articulo_create_or_update(request, **kwargs):
    #if request.user.is_authenticated:
        if request.user.perfil.idempresa.id == int(kwargs['id_empresa']) or request.user.is_staff:
            if kwargs['pk'] != '0':
                articulo = get_object_or_404(articulos, pk=kwargs['pk'])
            else:
                articulo = articulos()
                
            if request.method == 'POST':
                form = articulosForm(request.POST, instance=articulo)
                if form.is_valid():
                    form.save()
                    urlredirect = "/myapp/dashboard/" + str(request.user.perfil.idempresa.id)
                    return redirect(urlredirect)
            else:
                empresa = empresas.objects.get(id=int(kwargs['id_empresa']))
                articulo.idempresa = empresa
                familia = familias.objects.filter(idempresa=empresa).first()
                articulo.familia = familia
                articulo.fecha_precio = datetime.datetime.today().date()
                articulo.fecha_stock = datetime.datetime.today().date()

                form = articulosForm(instance=articulo, empresa_id=int(kwargs['id_empresa']))

        return render(request, 'myapp/articulo_form.html', {'form': form})
    
    #return redirect('login')

@login_required
def actualizar_precios(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        articulos_var = data.get('articulos', [])

        for articulo_data in articulos_var:
                articulo = articulos.objects.get(pk=articulo_data['id'])
                histo_mov = hist_movart()
                histo_mov.articulo = articulo
                histo_mov.fechamov = datetime.datetime.today().date()
                tipo_mov = 'Actualizacion precio'
                histo_mov.tipomov = tipo_mov
                histo_mov.precioactual = articulo.precio_venta
                histo_mov.porprecio = articulo_data['porcentaje']
                histo_mov.nuevoprecio = articulo_data['nuevo_precio']
                
                histo_mov.usuario = request.user
                histo_mov.save()
                
                articulo.precio_venta = articulo_data['nuevo_precio']
                articulo.fecha_precio = datetime.datetime.today().date()                
                articulo.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

@login_required
def guardar_movs_stock(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        empresa = data.get('empresa')
        idarticulo_var = data.get('id_articulo')
        tipomov_var = data.get('tipo_movimiento')
        motivo_var = data.get('motivo')
        cantidad_var = data.get('cantidad')
        preciocompra_var = data.get('precio_compra')
        numdoc_var = data.get('numdoc')

        articulo = articulos.objects.get(pk=idarticulo_var)
        histo_mov = hist_movart()
        histo_mov.articulo = articulo
        histo_mov.fechamov = datetime.datetime.today().date()
        mensaje = 'ATENCION!! Cantidad Entrada = 0, no se realizo ningun cambio'
        if cantidad_var !='':
            if tipomov_var == 'Regularizacion':                
                mensaje = 'Regularizacion de stock realizada con exito!'
                histo_mov.tipomov = motivo_var
                histo_mov.cantidad = cantidad_var
                histo_mov.stockactual = articulo.stock
                histo_mov.nuevostock = cantidad_var
                histo_mov.usuario = request.user
                histo_mov.save()
                    
                articulo.stock = cantidad_var
                articulo.fecha_stock = datetime.datetime.today().date()                
                articulo.save()
            elif tipomov_var == 'Entrada':
                mensaje = 'Entrada de stock realizada con exito!'
                histo_mov.tipomov = motivo_var
                histo_mov.cantidad = cantidad_var
                histo_mov.usuario = request.user
                histo_mov.stockactual = articulo.stock
                histo_mov.nuevostock = Decimal(cantidad_var) + articulo.stock
                histo_mov.usuario = request.user
                if motivo_var == "Compra":
                    histo_mov.numdoc = numdoc_var
                    histo_mov.precioactual = articulo.precio_compra
                    histo_mov.nuevoprecio = preciocompra_var

                    articulo.precio_compra = preciocompra_var
                    articulo.fecha_precio = datetime.datetime.today().date()
                    multi = Decimal(articulo.margen) *  Decimal(0.01) + 1
                    articulo.precio_venta = Decimal(preciocompra_var) * multi
                elif 'Traspaso' in motivo_var:
                    histo_mov.numdoc = empresa #este campo representa numero tique venta o numero de remito o factura de compra o nombre de empresa en caso de traspasos
                histo_mov.save()
                
                articulo.stock = Decimal(cantidad_var) + articulo.stock
                articulo.fecha_stock = datetime.datetime.today().date()                
                articulo.save()
            elif tipomov_var == 'Salida':
                mensaje = 'Salida de stock realizada con exito!'         
                histo_mov.tipomov = motivo_var
                histo_mov.numdoc = empresa #este campo representa numero tique venta o numero de remito o factura de compra o nombre de empresa en caso de traspasos
                histo_mov.cantidad = cantidad_var
                histo_mov.stockactual = articulo.stock
                histo_mov.nuevostock = articulo.stock - Decimal(cantidad_var)
                histo_mov.usuario = request.user
                histo_mov.save()
                    
                articulo.stock = articulo.stock - Decimal(cantidad_var)
                articulo.fecha_stock = datetime.datetime.today().date()                
                articulo.save()
            return JsonResponse({'success': True, 'modal': tipomov_var, 'message': mensaje})
        return JsonResponse({'success': True, 'modal': tipomov_var, 'message': mensaje})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

@login_required
def agregar_al_carrito(request, articulo_id, **kwargs):
    articulo = get_object_or_404(articulos, id=articulo_id)
    
    # Obtener el carrito de la sesión, o inicializarlo si no existe
    carrito = request.session.get('carrito', {})

    # Si el artículo ya está en el carrito, incrementar la cantidad
    if str(articulo_id) in carrito:
        carrito[str(articulo_id)]['cantidad'] += 1
    else:
        # Si no, agregar el artículo al carrito
        carrito[str(articulo_id)] = {
            'nombre': articulo.descripcion,
            'precio': float(articulo.precio_venta),
            'cantidad': 1
        }

    # Guardar el carrito en la sesión
    request.session['carrito'] = carrito
    request.session.modified = True
    return redirect('dashboard', kwargs['id_empresa'])  # Redirigir a la página de lista de artículos o carrito
# views.py

def ver_carrito(request, **kwargs):
    carrito = request.session.get('carrito', {})
    descuento_efectivo = obtener_descuento_efectivo()  # Lógica para obtener el descuento por pago en efectivo
    total = calcular_total_con_descuentos(carrito, descuento_efectivo)  # Lógica para calcular el total

    if request.method == 'POST':
        # Manejar el formulario de cierre de venta
        metodo_pago = request.POST.get('payment_method')
        descuento_adicional = request.POST.get('descuento_adicional')
        cerrar_venta(carrito, metodo_pago, descuento_adicional)  # Lógica para cerrar la venta
        return HttpResponseRedirect(reverse('venta_confirmada'))  # Redirigir a una página de confirmación

    return render(request, 'myapp/carrito.html', {
        'carrito': carrito,
        'descuento_efectivo': descuento_efectivo,
        'total': total, 
        'empresa' : kwargs['id_empresa']
    })
def obtener_descuento_efectivo():
    # Lógica para obtener el descuento por pago en efectivo
    return 10  # Ejemplo de valor fijo

def calcular_total_con_descuentos(carrito, descuento_efectivo):
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    return total  # Aplica descuentos aquí si es necesario

def cerrar_venta(carrito, metodo_pago, descuento_adicional):
    pass