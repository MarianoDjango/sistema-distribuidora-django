from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class formaspago(models.Model):
    FORMASP_CHOICES = [
        ('credito', 'Tarjeta Credito'), #sst codigo que indica que se SUMA al stock lo entrado por sistema
        ('debito', 'Tarjeta Debito'), #rst codigo que indica que se le debe RESTA al stock lo entrado por sistema
        ('contado', 'Efectivo'), #ast codigo que indica que se ACTUALIZA el stock a lo entrado por sistema
        ('transferencia', 'Transferencia/QR')  
    ]
    
    APLICA_DTO = ['contado']
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=FORMASP_CHOICES)
    aplicadto = models.BooleanField(default=0) #indica si la forma de pago aplica dto 0=False, 1=True
    aplicargo = models.BooleanField(default=0) #indica si forma de pago aplica recargo 0=False, 1=True

    def save(self, *args, **kwargs):
        # Determina si aplica descuento o recargo basado en `tipo`
        self.aplicadto = self.tipo in self.APLICA_DTO
        self.aplicargo = self.tipo in self.APLICA_DTO
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class tipomovimientos(models.Model):
    TIPO_CHOICES = [
        ('entradast', 'Compra'), #sst codigo que indica que se SUMA al stock lo entrado por sistema
        ('salidast', 'Venta'), #rst codigo que indica que se le debe RESTA al stock lo entrado por sistema
        ('regulast', 'Regularizacion Stock'), #ast codigo que indica que se ACTUALIZA el stock a lo entrado por sistema
        ('traspado', 'Traspaso empresas'),  
        ('subaprecio', 'Subir Precio'), #spr codigo que indica que se SUBE el precio el porcentaje entrado por pantalla
        ('bajaprecio', 'Bajar Precio'), #rpr codigo que indica que se SUBE el precio el porcentaje entrado por pantalla
    ]

    TIPO_CODIGO_MAP = {
        'entradast': 'sst',
        'salidast': 'rst',
        'regulast': 'ast',
        'traspado': 'rst',
        'subaprecio': 'spr',
        'bajaprecio': 'rpr',
    }

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    mov_st_pr = models.CharField(max_length=10, default='') #codgio de movimiento sobre stock o precio
    ''' codigos : sst codigo que indica que se SUMA al stock lo entrado por sistema
        rst codigo que indica que se le debe RESTA al stock lo entrado por sistema
        ast codigo que indica que se ACTUALIZA el stock a lo entrado por sistema
        spr codigo que indica que se SUBE el precio el porcentaje entrado por pantalla
        rpr codigo que indica que se SUBE el precio el porcentaje entrado por pantalla'''

    def save(self, *args, **kwargs):
        # Completa el campo `mov_st_pr` basado en `tipo`
        if self.tipo in self.TIPO_CODIGO_MAP:
            self.mov_st_pr = self.TIPO_CODIGO_MAP[self.tipo]
        super().save(*args, **kwargs)    

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class empresas(models.Model):
    name = models.CharField(max_length=255,blank=False, null=False)
    dtoefectvo = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)   # Porcentaje de descuento por pago en efectivo
    margen_emp = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Porcentaje de margen
    recargo_emp = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Porcentaje de recargo pago tarjeta
    
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
    precio_venta = models.DecimalField(max_digits =  11, decimal_places = 2, default=0)
    fecha_precio = models.DateField()
    stock = models.DecimalField(max_digits =  7, decimal_places = 2, default=0)
    fecha_stock = models.DateField()
    imagen = models.CharField(max_length = 250, blank=True)
    activo = models.BooleanField(default=True)
    comentarios = models.CharField(max_length = 250, blank=True)
    precio_compra = models.DecimalField(max_digits =  11, decimal_places = 2, default=0)
    margen = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Porcentaje de margen
    
    
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

class cabecera_venta(models.Model):
    fechav = models.DateField()    
    cliente = models.ForeignKey(clientes, on_delete=models.CASCADE, null=False)
    nomcliente = models.CharField(max_length = 50, default='') #este campo permite entrar un nombre cuando elcliente es el 0='generico'
    formapago = models.ForeignKey(formaspago, on_delete=models.CASCADE, null=False)
    dtoeftvo = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    otrodto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    recargo = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    imptotal = models.DecimalField(max_digits=13, decimal_places=2, default=0.00)

class hist_movart(models.Model):
    articulo = models.ForeignKey(articulos, on_delete=models.CASCADE, null=False)
    fechamov = models.DateField()
    tipomov = models.ForeignKey(tipomovimientos, on_delete=models.CASCADE, null=False)
    numdoc = models.CharField(max_length = 50, default=0) #este campo representa numero tique venta o numero de remito o factura de compra
    cantidad = models.DecimalField(max_digits =  7, decimal_places = 2, default=0.00)
    precioactual = models.DecimalField(max_digits =  11, decimal_places = 2, default=0) 
    porprecio = models.DecimalField(max_digits=5, decimal_places=2, default=0.00) #porcentaje de suba o baja de precio
    nuevoprecio = models.DecimalField(max_digits =  11, decimal_places = 2, default=0.00)
    stockactual = models.DecimalField(max_digits =  7, decimal_places = 2, default=0.00)
    nuevostock = models.DecimalField(max_digits =  7, decimal_places = 2, default=0)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
# Create your models here.


