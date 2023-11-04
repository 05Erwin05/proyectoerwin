from django.db import models
import uuid
import shortuuid
from django.db.models.signals import post_save
from django.dispatch import receiver


def conver_encode():
    u = uuid.uuid4()
    s = shortuuid.encode(u)
    return s


class Producto(models.Model):
    id_producto = models.CharField(primary_key=True,max_length=100,unique=True,default=conver_encode,editable=False)
    cod_producto=models.CharField(unique=True,max_length=100,blank=False,null=False,verbose_name='Código de producto',editable=False)
    nombre = models.CharField(max_length=155, blank=False, null=False,verbose_name="Nombre")
    detalle = models.TextField(max_length=555, blank=True, null=True,verbose_name="Detalle")
    categorias=models.ManyToManyField('Categoria',verbose_name='Categorias')
    costo = models.FloatField(default=0, blank=True, null=True,verbose_name="Costo")
    stock = models.IntegerField(default=0, blank=True, null=True,verbose_name="Stock")
    estado=models.BooleanField(default=False,verbose_name='Estado')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.id_producto:
            # Genera el código del producto solo si no tiene un ID asignado (es un nuevo producto)
            self.cod_producto = self.generate_cod_producto()
        super().save(*args, **kwargs)

    def generate_cod_producto(self):
        # Obtén la cantidad total de productos
        total_productos = Producto.objects.count()

        # Aumenta la cantidad total en 1 para obtener el próximo número
        new_number = total_productos + 1

        # Formatea el código del producto
        return f'CP{str(new_number).zfill(5)}'

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        db_table = "producto"

# Función para manejar la señal post_save
@receiver(post_save, sender=Producto)
def actualizar_cod_producto(sender, instance, **kwargs):
    # Verifica si el código de producto es diferente y lo guarda
    if not instance.cod_producto:
        instance.cod_producto = instance.generate_cod_producto()
        instance.save()


class Categoria(models.Model):
    id_categoria = models.CharField(primary_key=True,max_length=100,unique=True,default=conver_encode,editable=False)
    nombre = models.CharField(max_length=155, blank=False, null=False,verbose_name="Nombre")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta():
        verbose_name="Categoria"
        verbose_name_plural="Categorias"
        db_table="categoria"


class Compra(models.Model):
    id_compra = models.CharField(primary_key=True, max_length=100, unique=True, default=conver_encode, editable=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria", related_name="compras", blank=False, null=False)
    cantidad = models.IntegerField(default=1, blank=False, null=False, verbose_name="Cantidad")
    costo = models.FloatField(default=0, blank=False, null=False, verbose_name="Costo")
    total_compra = models.FloatField(default=0, blank=False, null=False, verbose_name="Total de la compra", editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_compra

    def save(self, *args, **kwargs):
        # Calcula el total de la compra antes de guardar
        self.total_compra = self.costo * self.cantidad
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        db_table = "compra"