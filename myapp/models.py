from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class empresas(models.Model):
    name = models.CharField(max_length=255,blank=False, null=False)

    def __str__(self):
        return f"{self.id} - {self.name}"

class perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, null=True, default=None)
    idempresa = models.ForeignKey(empresas, on_delete=models.CASCADE, null=True)
    
    def __str__(self): 
        return str(self.user)
    class Meta:
        ordering = ["nombre"]

class tipomovimientos(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('transferencia', 'Transferencia'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
    
class familias(models.Model):
    idempresa = models.ForeignKey(empresas, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length = 50, blank=True, null=True)

    def __str__(self):
        return str(self.id) + "-" + self.nombre

    class Meta:
        ordering = ["id"]
        verbose_name = "Familias"    

class articulos(models.Model):
    idempresa = models.ForeignKey(empresas, on_delete=models.CASCADE, null=True)
    codigobarras = models.CharField(max_length = 15, blank=False, null=False, default=0)
    familia = models.ForeignKey(familias, on_delete=models.CASCADE, null=True)
    descripcion = models.CharField(max_length = 200, blank=False, null=False)
    precio_venta = models.DecimalField(max_digits =  8, decimal_places = 2, default=0)
    fecha_precio = models.DateField()
    stock = models.DecimalField(max_digits =  4, decimal_places = 2, default=0)
    fecha_stock = models.DateField()
    imagen = models.CharField(max_length = 250, blank=True)
    activo = models.BooleanField(default=True)
    comentarios = models.CharField(max_length = 250, blank=True)
    precio_compra = models.DecimalField(max_digits =  8, decimal_places = 2, default=0)
    margen = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Porcentaje de margen
    dtoefectvo = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)   # Porcentaje de descuento por pago en efectivo
    
    def __str__(self):
        return self.descripcion

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ["-activo", "descripcion"]

class clientes(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Create your models here.
