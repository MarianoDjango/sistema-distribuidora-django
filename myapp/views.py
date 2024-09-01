from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .models import empresas, familias, articulos
import json
from django.http import JsonResponse, HttpResponse
from .forms import articulosForm
import datetime

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
            articles = articulos.objects.filter(familia=int(familia_id), activo=True).values('id', 'idempresa','descripcion', 'precio_venta', 'fecha_precio', 'stock', 'fecha_stock', 'familia' )
        else:
            articles = articulos.objects.filter(familia=int(familia_id), descripcion__icontains=nombre_var, activo=True).values('id', 'idempresa','descripcion', 'precio_venta', 'fecha_precio', 'stock', 'fecha_stock')
        familia = familias.objects.get(id=int(familia_id))
        recs.append(json_list)
        for articulo in articles:
            fila = '<tr style="cursor:hand;">'
            if articulo['idempresa'] == request.user.perfil.idempresa.id or request.user.is_staff:
                fila += '<td><a href="../../articulo/' + idempresa_var + '/' + str(articulo['id']) + '/">' + articulo['descripcion'] + '</a></td>'
                fila += '<td class="text-end"><a href="#">' + '{:,.2f}'.format(articulo['precio_venta']).replace(",", "@").replace(".", ",").replace("@", ".") + '</a></td>'
                fila += '<td class="text-center">' + str(articulo['fecha_precio']) + '</td>'
                fila += '<td class="text-end"><a href="#">' + '{:,.2f}'.format(articulo['stock']).replace(",", "@").replace(".", ",").replace("@", ".") + '</a></td>'
                fila += '<td class="text-center">' + str(articulo['fecha_stock']) + '</td>'
            
                fila += f'<td class="text-center"><input type="text" class="form-control" style="border-radius: 10px;" placeholder="Cant."></td>'
                fila += f'<td class="text-center"><button class="btn" style="background-color: #92dea3;"><i class="bi bi-cart-plus"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cart-plus" viewBox="0 0 16 16"><path d="M9 5.5a.5.5 0 0 0-1 0V7H6.5a.5.5 0 0 0 0 1H8v1.5a.5.5 0 0 0 1 0V8h1.5a.5.5 0 0 0 0-1H9z"/><path d="M.5 1a.5.5 0 0 0 0 1h1.11l.401 1.607 1.498 7.985A.5.5 0 0 0 4 12h1a2 2 0 1 0 0 4 2 2 0 0 0 0-4h7a2 2 0 1 0 0 4 2 2 0 0 0 0-4h1a.5.5 0 0 0 .491-.408l1.5-8A.5.5 0 0 0 14.5 3H2.89l-.405-1.621A.5.5 0 0 0 2 1zm3.915 10L3.102 4h10.796l-1.313 7zM6 14a1 1 0 1 1-2 0 1 1 0 0 1 2 0m7 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0"/></svg></i></button></td>'
                id_articulo = str(articulo['id'])
                fila += f'<td class="text-center"><div class="form-check"><input class="form-check-input" type="checkbox" value="" id="flexCheckDefault{id_articulo}"><label class="form-check-label" for="flexCheckDefault{id_articulo}"></label></div></td>'
            else:
                fila += '<td>'+ articulo['descripcion'] + '</td>'
                fila += '<td class="text-end">{:,.2f}'.format(articulo['precio_venta']).replace(",", "@").replace(".", ",").replace("@", ".") + '</td>'
                fila += '<td class="text-center">' + str(articulo['fecha_precio']) + '</td>'
                fila += '<td class="text-end">{:,.2f}'.format(articulo['stock']).replace(",", "@").replace(".", ",").replace("@", ".") + '</td>'
                fila += '<td class="text-center">' + str(articulo['fecha_stock']) + '</td>'

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
        if not self.request.user.is_authenticated:
            context = {}
        else:
            empresa_id = kwargs['id_empresa']
            empresa_obj = get_object_or_404(empresas, id=empresa_id)
            companies_var = empresas.objects.all()  # Obtenemos todas las empresas
            empresa_user = self.request.user.perfil.idempresa.id
            nomempresa_user = self.request.user.perfil.idempresa.name
            familias_var = familias.objects.filter(idempresa=empresa_id)
            familia = familias_var[0]
            
            context = {'empresas': companies_var, 'id_empresa':int(empresa_id),'nomempresa' : empresa_obj.name,  'id_familia' : familia.id, 'familia_nom' : familia.nombre }

        return render(self.request, self.template_name, context)

def articulo_create_or_update(request, **kwargs):
    if request.user.is_authenticated:
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
    
    return redirect('login')
