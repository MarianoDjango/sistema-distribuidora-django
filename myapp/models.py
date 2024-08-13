from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class empresas(models.Model):
    name = models.CharField(max_length=255,blank=False, null=False)

    def __str__(self):
        return self.name

class familias(models.Model):
    nombre = models.CharField(max_length = 50, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Familias"    

class articulos(models.Model):
    idempresa = models.ForeignKey(empresas, on_delete=models.CASCADE, null=True)
    codigobarras = models.CharField(max_length = 15, blank=False, null=False, default=0)
    familia = models.ForeignKey(familias, on_delete=models.CASCADE, null=True)
    descripcion = models.CharField(max_length = 200, blank=False, null=False)
    precio_venta = models.DecimalField(max_digits =  8, decimal_places = 2, default=0)
    fecha_precio = models.DateField()
    stock = models.DecimalField(max_digits =  8, decimal_places = 2, default=0)
    fecha_stock = models.DateField()
    imagen = models.CharField(max_length = 250, blank=True)
    activo = models.BooleanField(default=True)
    comentarios = models.CharField(max_length = 250, blank=True)

    def __str__(self):
        return self.descripcion

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ["-activo", "descripcion"]

# Create your models here.
