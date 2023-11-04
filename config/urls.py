# En el archivo urls.py en tu proyecto principal
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static



admin.site.site_header  =  "HUANCAPAMPA"  
admin.site.site_title  =  "Administracion"
admin.site.index_title  =  "PRODUCTOS DE ESTUCOS"

urlpatterns = [
    path('', admin.site.urls), 
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
