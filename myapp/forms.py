from .models import articulos, familias, empresas
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
                  'comentarios', 'precio_compra', 'margen', 'dtoefectvo']
        labels = {
            'dtoefectvo': 'Dto. Efectivo',
        }        
        widgets = {
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'familia': forms.Select(attrs={'class': 'form-select'}),  # Si familia se ve como input, prueba con Select
            'fecha_precio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_stock': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),
            'margen': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),
            'dtoefectvo': forms.NumberInput(attrs={'class': 'form-control', 'style': 'text-align: right;'}),
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

class articulosFormoksinformato(forms.ModelForm):
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
        
        if self.instance.pk:
            self.fields['fecha_precio'].initial = self.instance.fecha_precio
            self.fields['fecha_stock'].initial = self.instance.fecha_stock
        else:
            self.fields['fecha_precio'].initial = timezone.now().date()
            self.fields['fecha_stock'].initial = timezone.now().date()

class articulosFormxxxx(forms.ModelForm):
    '''fecha_precio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial= now().date()  # Esto establece la fecha de hoy como valor por defecto
    )
    fecha_stock = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=now().date()  # Esto establece la fecha de hoy como valor por defecto
    )'''

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
        
        if self.instance.pk:
            self.fields['fecha_precio'].initial = self.instance.fecha_precio
            self.fields['fecha_stock'].initial = self.instance.fecha_stock
        else:
            # Si es un nuevo registro, se asigna la fecha actual
            self.fields['fecha_precio'].initial = timezone.now().date()
            self.fields['fecha_stock'].initial = timezone.now().date()
        
        for field in self.fields:
            if field == 'familia':
                self.fields[field].widget.attrs.update({'class': 'form-select'})
            elif field == 'precio_venta' or field == 'precio_compra' or field == 'stock' or field == 'margen' or field == 'dtoefectvo':
                self.fields[field].widget.attrs.update({'class': 'form-control', 'style': 'text-align: right;'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_fecha_precio(self):
        fecha_precio = self.cleaned_data.get('fecha_precio')
        if fecha_precio:
            return fecha_precio.strftime('%Y-%m-%d')
        return fecha_precio

    def clean_fecha_stock(self):
        fecha_stock = self.cleaned_data.get('fecha_stock')
        if fecha_stock:
            return fecha_stock.strftime('%Y-%m-%d')
        return fecha_stock