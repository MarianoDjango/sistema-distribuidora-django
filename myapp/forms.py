from .models import articulos, familias
from django.forms import ModelForm, TextInput, Select, CheckboxInput
from django import forms
from django.core.exceptions import ValidationError


class articleForm(ModelForm):

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
            "precio_venta",
            "fecha_precio",
            "stock",
            "fecha_stock",
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
            "precio_venta",
            "fecha_precio",
            "stock",
            "fecha_stock",
            "activo",
        ]
        widgets = {
            'id': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'oninput' : 'validar()',
                'type' : 'number',
                'maxlength' : '15'
                }), 
            'dexcripcion': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 800px;',
                }),
            'familia': Select (attrs={
                'class': "form-select", 
                'style': 'max-width: 800px;',
                'placeholder': 'Familia',
                'onchange' : 'displayResult()'
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
                'placeholder': 'Fecha Stcok'
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


