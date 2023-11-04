from django.contrib import admin
from .models import Producto, Categoria,Compra

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('cod_producto', 'nombre', 'costo', 'stock', 'estado', 'created_at', 'updated_at')
    list_filter = ('categorias', 'estado')
    search_fields = ('cod_producto', 'nombre')
    ordering = ('-created_at',)

class CompraAdmin(admin.ModelAdmin):
    list_display = ['id_compra', 'categoria', 'cantidad', 'costo', 'total_compra', 'created_at', 'updated_at']
    search_fields = ['id_compra', 'categoria__nombre']  # Ajusta 'categoria__nombre' según la propiedad real de tu modelo de Categoria


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)
admin.site.register(Compra,CompraAdmin)