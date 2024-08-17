from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .models import empresas, familias, articulos
import json
from django.http import HttpResponse, Http404

def afterlogin( request, *args, **kwargs):
    idempresa = request.user.perfil.idempresa
    urlredirect = "/myapp/dashboard/" + str(idempresa.id) + "/"
    return redirect(urlredirect)

def famlias_empresa(request, **kwargs):
    empresa_id = request.GET['idempresa']
    familias_var = familias.objects.filter(idempresa=empresa_id)
    recs = []
    json_list = {}
    for fam in familias_var:
        fila = '<a href="javascript:void(0);" class="list-group-item border-end-0 d-inline-block text-truncate" data-bs-parent="#sidebar" onclick="ponerfamilia(' +  str(fam.id) + ' , ' +  fam.nombre + ')"><i class="bi bi-bootstrap"></i><span>' + fam.nombre + '</span></a>'
        json_list = {
            'fila': fila,
        }
        recs.append(json_list)    
    data = json.dumps(recs)
    return HttpResponse(data, 'application/json')

def articulos_famila(request, **kwargs):
    familia_id = request.GET['familia']
    nombre_var = request.GET['nombre']
    if nombre_var == "":
        articles = articulos.objects.filter(familia=int(familia_id)).values('descripcion', 'precio_venta', 'stock', 'familia')
    else:
        articles = articulos.objects.filter(familia=int(familia_id), descripcion__icontains=nombre_var).values('descripcion', 'precio_venta', 'stock')
    recs = []
    json_list = {}
    familia = familias.objects.get(id=int(familia_id))
    recs.append(json_list)
    for articulo in articles:
        fila = '<tr style="cursor:hand;">'
        fila += '<td>' + articulo['descripcion'] + '</td>'
        fila += '<td>' + str(articulo['precio_venta']) + '</td>'
        fila += '<td>' + str(articulo['stock']) + '</td>'
        json_list = {
            'fila': fila,
        }
        recs.append(json_list)
    
    data = json.dumps(recs)
    return HttpResponse(data, 'application/json')

class dashboard_view(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            context = {}
        else:
            companies_var = empresas.objects.all()  # Obtenemos todas las empresas
            empresa_user = self.request.user.perfil.idempresa.id
            familias_var = familias.objects.filter(idempresa=empresa_user)
            familia = familias_var[0]
            context = {'empresas': companies_var, 'id_empresa':int(empresa_user), 'id_familia' : familia.id, 'familia_nom' : familia.nombre }

        return render(self.request, 'myapp/dashboard.html', context)

def familias_por_empresa(request, *args, **kwargs):
    familias_var = familias.objects.filter(idempresa=kwargs['pk'])
    context = {'familias': familias_var}
    return render(request, 'myapp/familias.html', context)

def articulos_por_familia(request, *args, **kwargs):
    query = request.GET.get('search', '')  # Obtener el texto ingresado
    articles = articulos.objects.filter(familia_id=kwargs['id'], descripcion__icontains=query)
    context = {'articulos': articles}
    return render(request, 'myapp/dashboard.html', context)