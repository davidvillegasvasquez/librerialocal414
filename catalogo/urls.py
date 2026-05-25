from django.urls import path
from . import views
from django.contrib import admin #Aunque no se vé el uso del admin aquí, si no lo importo se presenta la excepción "LookupError: No installed app with label 'admin'".
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.Libros.as_view(), name='inicio'),
    #Urls de la api para ser consumida por clientes externos (android e iOS):
    path('api/', views.api_root),
    path('api/libros/', views.Libros.as_view(), name='libro-list'),         
    path('api/libros/<int:pk>/', views.LibroDetalle.as_view(), name='libro-detail'), 
    path('api/autores/', views.Autores.as_view(), name='autor-list'), 
    path('api/autores/<int:pk>/', views.AutorDetalle.as_view(), name='autor-detail'), 
    #Otros path:
    path('libros/isbn/', views.Libros.as_view(), name='isbn'),
    path('libros/isbn-busqueda/', views.Libros.as_view(), name='isbnConsulta'),
    path('libros/descargar-pdf/', views.descargar_pdf, name='descargar_pdf'),
    path('libros/<int:pk>/eliminar/', views.BorrarLibroHtml.as_view(), name='libro-eliminar'),
    path('autores/eliminar-autor/', views.Libros.as_view(), name='isbn'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
