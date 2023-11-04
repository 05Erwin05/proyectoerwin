from django.contrib import admin
from .models import Cliente,Venta

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'zona', 'av_calle', 'numero', 'genero', 'estado', 'created_at', 'updated_at')
    list_filter = ('genero', 'estado')
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'telefono')
    ordering = ('-created_at',)


class VentaAdmin(admin.ModelAdmin):
    list_display = ['cod_venta', 'cantidad', 'total_venta', 'cliente', 'fecha_venta', 'estado', 'categoria']
    search_fields = ['cod_venta', 'cliente']
    list_filter = ['estado', 'categoria']

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Venta, VentaAdmin)
