from django.shortcuts import render

# Create your views here.
from .models import empresas, familias

def dashboard_view(request, *args, **kwargs):
    companies_var = empresas.objects.all()  # Obtenemos todas las empresas
    familias_var = familias.objects.filter(idempresa=kwargs['pk'])
    context = {'empresas': companies_var, 'familias': familias_var}
    return render(request, 'myapp/dashboard.html', context)

def familias_por_empresa(request, *args, **kwargs):
    familias_var = familias.objects.filter(idempresa=kwargs['pk'])
    context = {'familias': familias_var}
    return render(request, 'myapp/familias.html', context)
