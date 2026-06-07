from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Agregamos los campos personalizados para poder visualizarlos y editarlos
    model = CustomUser
    #Se debe explicitar el orden, ya que usamos el usuario personalizado con email:
    
    ordering = ('email',)
    list_display = ['email', 'first_name', 'last_name', 'is_staff',]
    search_fields = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'creador')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}), # Remove fields if your model doesn't have them
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
   
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'), # Recuerde que estos son los únicos campos para agregar nuevo usuario. password2 se refiere a la verificación que pide de volver a colocar el password para verificar.
        }),
    )
   
    
admin.site.register(CustomUser, CustomUserAdmin)

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
