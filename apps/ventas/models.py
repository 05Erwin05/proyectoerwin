from django.db import models
import uuid
import shortuuid
from apps.compras.models import Categoria,Producto
from django.db.models.signals import post_save
from django.dispatch import receiver



def conver_encode():
    u = uuid.uuid4()
    s = shortuuid.encode(u)
    return s

CHOICES_GENERO=[
    ('Femenino','Femenino'),
    ('Masculino','Masculino'),
]

class Cliente(models.Model):
    id_cliente = models.CharField(primary_key=True,max_length=100,unique=True,default=conver_encode,editable=False)
    nombre = models.CharField(max_length=155, blank=False, null=False,verbose_name="Nombre")
    apellido_paterno = models.CharField(max_length=155, blank=False, null=False,verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=155, blank=False, null=False,verbose_name="Apellido Materno")
    telefono = models.CharField(max_length=255, blank=True, null=True,verbose_name="Telefono")
    zona = models.CharField(max_length=100, blank=True, null=True,verbose_name="Zona")
    av_calle = models.CharField(max_length=100, blank=True, null=True,verbose_name="Avenida/Calle")
    numero = models.IntegerField(default=0, blank=True, null=True,verbose_name="Número")
    genero = models.CharField(max_length = 125,verbose_name="Género",choices=CHOICES_GENERO,blank=False,null=False)
    estado=models.BooleanField(default=False,verbose_name='Estado')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre+' '+self.apellido_paterno+' '+self.apellido_materno
    
    class Meta():
        verbose_name="Cliente"
        verbose_name_plural="Clientes"
        db_table="cliente"


class Venta(models.Model):
    id_venta = models.CharField(primary_key=True, max_length=100, unique=True, default=conver_encode, editable=False)
    cod_venta = models.CharField(max_length=100, unique=True, default=conver_encode, editable=False)
    cantidad = models.IntegerField(default=1, blank=False, null=False, verbose_name="Cantidad")
    total_venta = models.FloatField(default=0, blank=False, null=False, verbose_name="Total de venta", editable=False)
    cliente = models.ForeignKey(Cliente, max_length=255, blank=False, null=False, on_delete=models.CASCADE, related_name="ventas", verbose_name="Cliente")
    fecha_venta = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de venta")
    estado = models.CharField(max_length=20, choices=[('Venta', 'Venta'), ('Pedido', 'Pedido')], default='Venta', verbose_name="Estado")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria", related_name="ventas", blank=False, null=False)
    producto = models.ForeignKey(Producto, max_length=255, blank=False, null=False, on_delete=models.CASCADE, related_name="ventas", verbose_name="Producto")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cod_venta

    def save(self, *args, **kwargs):
        if not self.id_venta:
            # Genera el código de venta solo si no tiene un ID asignado (es una nueva venta)
            self.cod_venta = self.generate_cod_venta()
        # Calcula el total de venta antes de guardar
        self.total_venta = self.cantidad * self.producto.costo  # Usar el costo del producto directamente
        super().save(*args, **kwargs)

    def generate_cod_venta(self):
        # Obtén la cantidad total de ventas
        total_ventas = Venta.objects.count()

        # Aumenta la cantidad total en 1 para obtener el próximo número
        new_number = total_ventas + 1

        # Formatea el código de la venta
        return f'CV{str(new_number).zfill(5)}'


    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        db_table = "venta"

# Función para manejar la señal post_save
@receiver(post_save, sender=Venta)
def actualizar_cod_venta(sender, instance, **kwargs):
    # Verifica si el código de venta es diferente y lo guarda
    if not instance.cod_venta:
        instance.cod_venta = instance.generate_cod_venta()
        instance.save()