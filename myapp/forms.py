from .models import articulos, familias, empresas
from django.forms import ModelForm, TextInput, Select, CheckboxInput
from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class articulosForm(forms.ModelForm):
    fecha_precio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial= now().date()  # Esto establece la fecha de hoy como valor por defecto
    )
    fecha_stock = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=now().date()  # Esto establece la fecha de hoy como valor por defecto
    )

    class Meta:
        model = articulos
        fields = ['idempresa', 'codigobarras', 'familia', 'descripcion', 'precio_venta', 
                  'fecha_precio', 'stock', 'fecha_stock', 'imagen', 'activo', 
                  'comentarios', 'precio_compra', 'margen', 'dtoefectvo']
        labels = {
            'dtoefectvo': 'Dto. Efectivo',
        }        
        widgets = {
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_precio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_stock': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):
        super(articulosForm, self).__init__(*args, **kwargs)
        if 'idempresa' in self.data:
            try:
                idempresa_id = int(self.data.get('idempresa'))
                self.fields['familia'].queryset = familias.objects.filter(idempresa=idempresa_id).order_by('nombre')
            except (ValueError, TypeError):
                self.fields['familia'].queryset = familias.objects.none()
        elif self.instance.pk:
            self.fields['familia'].queryset = self.instance.idempresa.familias_set.order_by('nombre')
        
        self.fields['fecha_precio'].initial = self.instance.fecha_precio.strftime('%Y-%m-%d')
        self.fields['fecha_stock'].initial = self.instance.fecha_stock.strftime('%Y-%m-%d')
        
        for field in self.fields:
            if field == 'familia':
                self.fields[field].widget.attrs.update({'class': 'form-select'})
            elif field == 'precio_venta' or field == 'precio_compra' or field == 'stock' or field == 'margen' or field == 'dtoefectvo':
                self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'text-align: right;'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

class articleFormold(ModelForm):

    #def __init__(self,*args,**kwargs):
    #    super(articleForm,self).__init__(*args)

    # create meta class
    class Meta:

        # specify model to be used
        model = articulos
        fields = [
            "id",
            "descripcion",
            "familia",
            "precio_compra",
            "margen",
            "precio_venta",
            "fecha_precio",
            "stock",
            "fecha_stock",
            "dtoefectvo",
            "activo",
        ]
        widgets = {
            'id': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'oninput' : 'validar()',
                'readonly' : 'readonly'
                }), 
            'descripcion': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 800px;',
                }),
            'familia': Select (attrs={
                'class': "form-select", 
                'style': 'max-width: 800px;',
                'placeholder': 'Familia',
                'onchange' : 'displayResult()'
                }),
            'precio_compra': TextInput(attrs={
                'class': "form-control", 
                'style': 'text-align: right;',
                'placeholder': 'Precio Compra'
                }),
            'margen': TextInput(attrs={
                'class': "form-control", 
                'style': 'text-align: right;',
                'placeholder': 'Margen'
                }),
            'precio_venta': TextInput(attrs={
                'class': "form-control", 
                'style': 'text-align: right;',
                'placeholder': 'Precio Venta'
                }),
            'fecha_precio': TextInput(attrs={
                'class': "form-control", 
                'style': 'text-align: right;',
                'placeholder': 'Fecha Precio'
                }),
            'stock': TextInput(attrs={
                'class': "form-control", 
                'style': 'text-align: right;',
                'placeholder': 'Stock'
                }),
            'fecha_stock': TextInput(attrs={
                'class': "form-control", 
                'style': 'text-align: right;',
                'placeholder': 'Fecha Stock'
                }),
            'activo': CheckboxInput(attrs={
                'class': "form-check-input", 
                'type' : "checkbox",
                'role' : "switch"
                }),
        }
    def __init__(self, *args, **kwargs):
        super(articulosForm, self).__init__(*args, **kwargs)
        if 'empresa' in self.data:
            try:
                empresa_id = int(self.data.get('empresa'))
                self.fields['familia'].queryset = familias.objects.filter(idempresa=empresa_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # Invalida empresa_id, mostrar un queryset vacío
        elif self.instance.pk:
            self.fields['familia'].queryset = self.instance.empresas.familia_set.order_by('id')
    
    def clean(self):
        #codigo = self.cleaned_data['codigo']
        nombre = self.cleaned_data['nombre']
        if nombre == '':
            raise self.ValidationError({'fecha':nombre.error})

        return self.cleaned_data

class NewarticleForm(ModelForm):

    #def __init__(self,*args,**kwargs):
    #    super(articleForm,self).__init__(*args)

    # create meta class
    class Meta:

        # specify model to be used
        model = articulos
        fields = [
            "id",
            "descripcion",
            "familia",
            "precio_compra",
            "margen",
            "precio_venta",
            "fecha_precio",
            "stock",
            "fecha_stock",
            "dtoefectvo",
            "activo",
        ]
        widgets = {
            'id': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'oninput' : 'validar()',
                'readonly' : 'readonly'
                }), 
            'descripcion': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 800px;',
                }),
            'familia': Select (attrs={
                'class': "form-select", 
                'style': 'max-width: 800px;',
                'placeholder': 'Familia',
                'onchange' : 'displayResult()'
                }),
            'precio_compra': TextInput(attrs={
                'class': "form-control", 
                'style': 'text-align: right;',
                'placeholder': 'Precio Compra'
                }),
            'margen': TextInput(attrs={
                'class': "form-control", 
                'style': 'text-align: right;',
                'placeholder': 'Margen'
                }),
            'precio_venta': TextInput(attrs={
                'class': "form-control", 
                'style': 'text-align: right;',
                'placeholder': 'Precio Venta'
                }),
            'fecha_precio': TextInput(attrs={
                'class': "form-control", 
                'style': 'text-align: right;',
                'placeholder': 'Fecha Precio'
                }),
            'stock': TextInput(attrs={
                'class': "form-control", 
                'style': 'text-align: right;',
                'placeholder': 'Stock'
                }),
            'fecha_stock': TextInput(attrs={
                'class': "form-control", 
                'style': 'text-align: right;',
                'placeholder': 'Fecha Stock'
                }),
            'activo': CheckboxInput(attrs={
                'class': "form-check-input", 
                'type' : "checkbox",
                'role' : "switch"
                }),
        }

    def clean(self):
        #codigo = self.cleaned_data['codigo']
        nombre = self.cleaned_data['descripcion']
        if nombre == '':
            raise self.ValidationError({'fecha':nombre.error})

        return self.cleaned_data

class familiaForm(ModelForm):

    #def __init__(self,*args,**kwargs):
    #    super(articleForm,self).__init__(*args)

    # create meta class
    class Meta:

        # specify model to be used
        model = familias
        fields = [
            "id",
            "nombre",
        ]
        widgets = {
            'instance.id': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 800px;',
                'readonly' : 'readonly'
                }),
            'nombre': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 800px;',
                }),
        }

    def clean(self):
        #codigo = self.cleaned_data['codigo']
        nombre = self.cleaned_data['nombre']
        if nombre == '':
            raise self.ValidationError({'nombre':nombre.error})

        return self.cleaned_data


