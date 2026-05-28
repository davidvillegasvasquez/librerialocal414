from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import Autor, Genero, Libro, LibroInstancia, Lenguaje

# Define the admin class
@admin.register(Autor)
class AutorAdministrador(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'nacimiento', 'muerte')
    #list_display_links = None (atributo que le quita el link al primer campo)
    #fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Register the admin class with the associated model
#admin.site.register(Autor, AutorAdministrador) 

#Nota: cuando se usa el decorador @admin.register(modelo), no se usa la proposición de registro de asociación del modelo con la nueva clase personalizada, de lo contrario arroja el error de que ya ha sido registrado dicho modelo.

# Register the Admin classes for Book using the decorator
@admin.register(Libro)
class LibroAdministrador(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'mostrar_genero')

@admin.register(LibroInstancia)
class LibroInstanciaAdmin(admin.ModelAdmin):
    list_display = ('libro', 'imprenta', 'id','estatus')
    list_filter = ('estatus', 'debidoderegresar')
    
    fieldsets = ((None, {'fields': ('libro', 'imprenta', 'id')}),('Disponibilidad', {'fields': ('estatus', 'debidoderegresar', 'prestatario')}),)

#Hacemos registros sencillos (no es necesario hacer una clase para ellos), para modelos sencillos de un sólo campo:

admin.site.register(Genero)
admin.site.register(Lenguaje)
