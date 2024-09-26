from .models import articulos, familias, empresas, clientes
from django.forms import ModelForm, TextInput, Select, CheckboxInput
from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils import timezone

class articulosForm(forms.ModelForm):
    fecha_precio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'],
        initial= now().date()
    )
    fecha_stock = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'],
        initial= now().date()
    )

    class Meta:
        model = articulos
        fields = ['idempresa', 'codigobarras', 'familia', 'descripcion', 'precio_venta', 
                  'fecha_precio', 'stock', 'fecha_stock', 'imagen', 'activo', 
                  'comentarios', 'precio_compra', 'margen', 'margen2']
        widgets = {
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'familia': forms.Select(attrs={'class': 'form-select'}),  # Si familia se ve como input, prueba con Select
            'fecha_precio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_stock': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),
            'margen': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),
            'margen2': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),
        }
    
    def __init__(self, *args, **kwargs):
        empresa_id = kwargs.pop('empresa_id', None)
        super(articulosForm, self).__init__(*args, **kwargs)
        if empresa_id:
            try:
                self.fields['familia'].queryset = familias.objects.filter(idempresa=empresa_id).order_by('nombre')
            except (ValueError, TypeError):
                self.fields['familia'].queryset = familias.objects.none()
        elif self.instance.pk:
            self.fields['familia'].queryset = self.instance.idempresa.familias_set.order_by('nombre')
        
        if self.instance.pk:
            self.fields['fecha_precio'].initial = self.instance.fecha_precio
            self.fields['fecha_stock'].initial = self.instance.fecha_stock
        else:
            self.fields['fecha_precio'].initial = timezone.now().date()
            self.fields['fecha_stock'].initial = timezone.now().date()

        # Asegúrate de que todos los campos tengan la clase form-control
        for field in self.fields:
            if not isinstance(self.fields[field].widget, forms.CheckboxInput):
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        self.fields['familia'].label_from_instance = lambda obj: obj.nombre                

class clientesForm(forms.ModelForm):

    class Meta:
        model = clientes
        fields = ['idempresa', 'nombre', 'apellido', 'email', 'telefono', 
                  'direccion', 'ciudad', 'provincia', 'codigo_postal', 
                  'activo']
        widgets = {
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        empresa_id = kwargs.pop('empresa_id', None)
        super(clientesForm, self).__init__(*args, **kwargs)

        # Asegúrate de que todos los campos tengan la clase form-control
        for field in self.fields:
            if not isinstance(self.fields[field].widget, forms.CheckboxInput):
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        
