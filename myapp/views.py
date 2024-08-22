from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .models import empresas, familias, articulos
import json
from django.http import HttpResponse
from .forms import articulosForm, NewarticleForm

def index(request):
    return render(request, 'index.html')

def afterlogin( request, *args, **kwargs):
    idempresa = request.user.perfil.idempresa
    urlredirect = "/myapp/dashboard/"
    return redirect(urlredirect)

def famlias_empresa(request, **kwargs):
    empresa_id = request.GET['idempresa']
    familias_var = familias.objects.filter(idempresa=empresa_id)
    recs = []
    json_list = {}
    for fam in familias_var:
        fila = f'<a href="javascript:void(0);" class="list-group-item border-end-0 d-inline-block text-truncate" data-bs-parent="#sidebar" onclick="ponerfamilia({fam.id}, \'{fam.nombre}\')"><span>{fam.nombre}</span></a>'
        json_list = {
            'fila': fila,
        }
        recs.append(json_list)    
    data = json.dumps(recs)
    return HttpResponse(data, 'application/json')

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
            fila += '<td><a href="../articulo/' + str(articulo['id']) + '/">' + articulo['descripcion'] + '</a></td>'
            fila += '<td class="text-end"><a href="#">' + '{:,.2f}'.format(articulo['precio_venta']).replace(",", "@").replace(".", ",").replace("@", ".") + '</a></td>'
            fila += '<td class="text-center">' + str(articulo['fecha_precio']) + '</td>'
            fila += '<td class="text-end"><a href="#">' + '{:,.2f}'.format(articulo['stock']).replace(",", "@").replace(".", ",").replace("@", ".") + '</a></td>'
            fila += '<td class="text-center">' + str(articulo['fecha_stock']) + '</td>'
            if str(articulo['idempresa']) == idempresa_var:
                fila += f'<td class="text-center"><input type="text" class="form-control" style="border-radius: 10px;" placeholder="Cant."></td>'
                fila += f'<td class="text-center"><button class="btn" style="background-color: #92dea3;"><i class="bi bi-cart-plus"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-cart-plus" viewBox="0 0 16 16"><path d="M9 5.5a.5.5 0 0 0-1 0V7H6.5a.5.5 0 0 0 0 1H8v1.5a.5.5 0 0 0 1 0V8h1.5a.5.5 0 0 0 0-1H9z"/><path d="M.5 1a.5.5 0 0 0 0 1h1.11l.401 1.607 1.498 7.985A.5.5 0 0 0 4 12h1a2 2 0 1 0 0 4 2 2 0 0 0 0-4h7a2 2 0 1 0 0 4 2 2 0 0 0 0-4h1a.5.5 0 0 0 .491-.408l1.5-8A.5.5 0 0 0 14.5 3H2.89l-.405-1.621A.5.5 0 0 0 2 1zm3.915 10L3.102 4h10.796l-1.313 7zM6 14a1 1 0 1 1-2 0 1 1 0 0 1 2 0m7 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0"/></svg></i></button>''</td>'
                fila += f'<td class="text-center"><div class="form-check"><input class="form-check-input" type="checkbox" value="" id="flexCheckDefault"><label class="form-check-label" for="flexCheckDefault"></label></div></td>'

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
            empresa = str(companies_var[0]).split((" - ")[1])
            context = {'empresas': companies_var, 'id_empresa':int(empresa_user),'nomempresa' : empresa[1],  'id_familia' : familia.id, 'familia_nom' : familia.nombre }

        return render(self.request, 'myapp/dashboard.html', context)

def articulo_create_or_update(request, pk=None):
    if pk:
        articulo = get_object_or_404(articulos, pk=pk)
    else:
        articulo = articulos()

    if request.method == 'POST':
        form = articulosForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('myapp/dashboard.html')
    else:
        form = articulosForm(instance=articulo)

    return render(request, 'myapp/articulo_form.html', {'form': form})

class articleView(View,LoginRequiredMixin):
    model = articulos
    form_class = articulosForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        #context = {'form': form}
        if self.request.user.is_authenticated:
        #raise Http404("Poll does not exist")
        #return render(request, "polls/detail.html", {"poll": p}) 
            try:
                articulo = articulos.objects.get(id=kwargs['pk'])
                form = self.form_class(instance=articulo)
                imagen = articulo.imagen
                doesnexist = False
            except articulos.DoesNotExist:
                articulo = articulos(id=kwargs['pk'], descripcion='')
                form = NewarticleForm(instance=articulo)
                doesnexist = True                
        else:
            articulo = None
            form = self.form_class(instance=articulo)
        return render(request, 'myapp/article_form.html', {'form': form, 'active' : 'Articulos', 'doesentexist' : doesnexist} )

