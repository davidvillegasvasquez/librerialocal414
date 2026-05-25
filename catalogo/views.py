from django.shortcuts import redirect, render
from .models import Libro, Autor, LibroInstancia, Genero
#Imprimir pdf:
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from django.contrib.auth.models import Group, User
from django.urls import reverse

#Rest framework:

from .serializadores import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication

class Libros(generics.ListCreateAPIView):
    """
    Vista de endpoint de tipo generics.ListCreateAPIView, serializada con serializers.HyperlinkedModelSerializer, para listar todos los libros (list) usando el método http get, o crear(create) uno nuevo con el método http post.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SerializadorLibro
    # Orden importa: primero HTML, luego JSON
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    #Gestionamos el tipo de permiso: sobrescribimos el método get_permissions(self). 
    #Esto te permite evaluar la solicitud (request), la URL o los parámetros del usuario y devolver una lista de clases de permiso diferentes en tiempo de ejecución.
    
    def get_permissions(self):       
        #Instancia y devuelve la lista de permisos que requiere esta vista.   
        if self.request.method == 'POST':
            # Solo administradores pueden crear
            self.permission_classes = [permissions.IsAdminUser]
        else:
            # Cualquiera puede listar
            self.permission_classes = [permissions.AllowAny]
            
        return super().get_permissions()
    
    def get_template_names(self):
        # Obtiene el nombre de la plantilla del parámetro de consulta (?template=...)
        #El error que tuve de enviar valores de parámetros de consulta url entrecomillados (por ej: ?plantilla='catalogo/todosLosLibros.html') me había causado el problema de que la plantilla no se encontraba:
        template_name = self.request.query_params.get('plantilla', None)
         
        if template_name is not None:#Nos ayuda con presentar la vista inicial.
            return [template_name]
        # Plantilla por defecto si no viene el parámetro
        return ['base1-inicio.html']
    
    def get_queryset(self):
        titulo=self.request.query_params.get('titulo', None)
        isbn=self.request.query_params.get('isbn', None)
 
        if titulo:
            queryset = Libro.objects.filter(titulo=titulo)
        elif isbn:   
            queryset = Libro.objects.filter(isbn=isbn)
        else:
            queryset=Libro.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        # Utiliza el serializador para validar y guardar los datos
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # --- Elige una de estas opciones de redirección ---
        # Opción 1: Redirigir a la vista de detalle del objeto (necesitas pasar el pk/id)
        # Obtiene la instancia recién creada
        #instance = serializer.instance
        #return redirect('nombre-de-tu-url-detalle', pk=instance.pk)

        # Opción 2: Redirigir a la vista de lista de objetos
        return redirect('libro-list')
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        #Antes de todo, evaluamos si la petición es API (JSON), devuelve la respuesta JSON
        if request.accepted_renderer.format == 'json':
            return response
        # Si es navegador, devuelve la plantilla con los datos. response.data es
 #un diccionario que contiene el campo o clave  'results', que es una lista de diccionarios, cuyo cada diccionario representa un registro o fila de cada libro, con los campos: url, id, titulo, autor, descripción e isbn. 
        queryset = self.get_queryset()
        seriali = self.serializer_class(context={'request': request})
        contexto = {
            'datos': response.data,
            'len': len(response.data), #response.data es una lista.
            'cant': queryset.count(),
            'seriali': seriali,
        }
        
        return Response(contexto, template_name=self.get_template_names()[0])

class LibroDetalle(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista de endpoint de tipo generics.RetrieveUpdateDestroyAPIView, serializada con serializers.HyperlinkedModelSerializer, para recuperar un libro(retrieve), actualizarlo(update), o eliminarlo(destroy).
    """
    queryset = Libro.objects.all()
    serializer_class = SerializadorLibro
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        #Primero lo primero: vemos que tipo de solicitud es:
        if request.accepted_renderer.format == 'json':
            return response
       
        instance = self.get_object() 
        seriali = self.get_serializer(instance)

        contexto = {
            #'objeto':
            'datos': response.data,
            'var_ext': "Hola desde la vista", 
            'seriali': seriali,
        }
        return Response(contexto)

    def get_template_names(self):
        template_name = self.request.query_params.get('plantilla', None)
        if template_name is not None:#Nos ayuda con presentar la vista inicial.
            return [template_name]
        # Plantilla por defecto si no viene el parámetro
        return ['catalogo/libro_detail.html']

    # Sobreescribir post para manejar la actualización desde form
    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('libro-list') #Response({'seriali': serializer, 'instance': instance})
        return Response({'seriali': serializer, 'instance': instance}, template_name='libro_actualizar.html')
    
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

class BorrarLibroHtml(DeleteView):
    model = Libro
    success_url = reverse_lazy('libro-list') # A dónde ir tras borrar
    #template_name = 'libro_confirm_delete.html' # HTML de confirmación

class PaginacionAutores(PageNumberPagination):
    page_size = 2  # Solo 2 elementos para esta vista

class Autores(generics.ListCreateAPIView):
    serializer_class = SerializadorAutor
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    #pagination_class = PaginacionAutores

    def get_permissions(self):
        """
        Instancia y devuelve la lista de permisos que requiere esta vista.
        """
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        # Utiliza el serializador para validar y guardar los datos
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return redirect('autor-list')
    
    def get_template_names(self):
        template_name = self.request.query_params.get('plantilla', None)
        if template_name is not None:#Nos ayuda con presentar la vista inicial.
            return [template_name]
        # Plantilla por defecto si no viene el parámetro
        return ['catalogo/autor_list.html']
    
    def get_queryset(self):
        titulo = self.request.query_params.get('titulo', None)
        isbn = self.request.query_params.get('isbn', None)
        if titulo is not None:
            queryset = Libro.objects.filter(titulo='Canaima')
        elif isbn is not None:
            queryset = Libro.objects.filter(isbn='4077862365395')
        else:
            queryset = Autor.objects.all()
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Si la petición es API (JSON), devuelve la respuesta JSON
        if request.accepted_renderer.format == 'json':
            return response
         
        queryset = self.get_queryset()
        seriali = self.serializer_class()
        contexto = {
            'datos': response.data,
            'cant': queryset.count(),
            'seriali': seriali,
        }
        
        return Response(contexto, template_name=self.get_template_names()[0])

class AutorDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = SerializadorAutor
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        #Primero lo primero: vemos que tipo de solicitud es:
        if request.accepted_renderer.format == 'json':
            return response
       
        instance = self.get_object() 
        seriali = self.get_serializer(instance)

        contexto = {
            'datos': response.data, 
            'seriali': seriali,
        }
        return Response(contexto)

    def get_template_names(self):
        template_name = self.request.query_params.get('plantilla', None)
        if template_name is not None:#Nos ayuda con presentar la vista inicial.
            return [template_name]
        # Plantilla por defecto si no viene el parámetro
        return ['catalogo/autor_detail.html']

#Hacemos un pundo de entrada para nuestra api:
from rest_framework.decorators import api_view

@api_view(["GET", "POST"])
def api_root(solicitud, formato=None):
    return Response(
        {  
            "libros": reverse("libro-list", request=request, format=format),
            "autores": reverse("autor-list", request=request, format=format),
        }
    )

def descargar_pdf(request):
    # 1. Obtener datos de la base de datos (ej. búsqueda)
    resultados = Libro.objects.all() 

    # 2. Renderizar HTML con los datos
    html_string = render_to_string('plantilla_pdf.html', {'resultados': resultados})

    # 3. Generar PDF
    html = HTML(string=html_string)
    result = html.write_pdf()

    # 4. Crear respuesta HTTP para descarga
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="resultados.pdf"'
    return response
