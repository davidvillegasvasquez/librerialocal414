from django.urls import path
from . import views
from django.contrib import admin #Aunque no se vé el uso del admin aquí, si no lo importo se presenta la excepción "LookupError: No installed app with label 'admin'".
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.inicio, name='vistaHome'), 
    path('libros/', views.LibroVistaLista.as_view(), name='todosLoslibros'),      path('libros/conbarbara', views.LibroVistaListaConBarbara.as_view(), name='librosConBarbara'), 
    path('libro/<int:pk>', views.VistaDetalleLibro.as_view(), name='detallesDeLibro'), 
    path('autores/', views.VistaListaGenAutores.as_view(), name='toditicosLosAutores'), 
    path('autor/<int:pk>', views.VistaDetalladaGenAutor.as_view(), name='autorDetalles'),  
    path('reseteoContSesiones', views.borrarConteoVisitas, name='resetearVisitas'),
    path('LibrosEnManosDelUsuario/<str:username>', views.ListaLibrosPrestadosAlUsuario.as_view(), name='misLibrosalquilados'),
    path('TodosLosLibrosActualmenteAlquilados/', views.ListaDeLibrosPrestadosActualmente.as_view(), name='librosAlquiladosActualmente'),
    path('libro/<uuid:claveprimaria>/renovacion/', views.renovacionLibroPorLibrero, name='renovDeLibroPorLibrero'),
    path('autor/crear/', views.CrearAutor.as_view(), name='crearautorini'),
    path('autor/<int:pk>/actualizar/', views.ActualizarAutor.as_view(), name='actualizarEsteAutor'), path('autor/<int:pk>/borrar/', views.BorrarAutor.as_view(), name='borrar-autor'),
    path('libro/crear/', views.CrearLibro.as_view(), name='crearlibro'),
    path('libro/<int:pk>/actualizar/', views.ActualizarLibro.as_view(), name='actualizarLibro'), path('libro/<int:pk>/borrar/', views.BorrarLibro.as_view(), name='borrarlibro'),
    path('ejemUsoSelectOptionsW3.css/', views.goTovistaGenDetailsAutorFromSelect, name='irAautorDetailsDesdeUnSelect'),
    path('irAdetalleAutorDesdeFormulario/', views.irAdetalleAutorDesdeForm, name='autorDetailDesdeForm'),]

#Ejemplos de cómo usar una función anónima lambda en lugar de usar vistas en views.py :
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

urlpatterns += [path('vistaDeFuncionAnonimaParaRedirigirAunaUrl/', lambda solicitudQueNoDaraParametros: HttpResponseRedirect(reverse('todosLoslibros')), name='redirigiendoA-listaDelibros'),]

#Note que podemos usar elementos html dentro de la pseudoplantilla que usamos en la función anónima lambda. Lo que no pudimo meter fue una etiqueta url django para ir a home: {% url 'vistaHome' %}
urlpatterns += [path('UsandoUnHttpResponseSinPlantillaNiVista/', lambda solicitudcualquiera: HttpResponse("<p>-----Saludos!!!</p><a href='/catalogo/'>Ir a home</a>"), name='UsarUnHttpResponseSinPlantillaNiVista'),]

urlpatterns += [
    path('formChoiceFieldAutorYsusLibrosJS/', views.autorYsusLibrosChoiceFieldJS, name='formModelChoiceFieldAutorYsusLibrosJS'),
    path('formChoiceFieldAutorYsusLibrosFormTools/', views.AutorYsusLibrosChoiceFielFormTools.as_view(), name='formToolsAutorYsusLibros'),
    path('navAutorYsusLibrosConJS/', views.navDetailAutorYSusLibros, name='navAutorYsusLibJS'),
    path('navAutorYsusLibrosConW3JS/', views.navDetailAutorYSusLibW3JS, name='navAutorYsusLibW3JS'),
    path('navAutorYsusLibrosConW3JSauxiliar/', views.auxParaUsarW3jsIncludeHTMLEnAutorYsusLib, name='navAutorYsusLibW3JSauxiliar'),
    path('navAutorYsusLibrosConHTMX/', views.navDetailAutorYSusLibHTMX, name='navAutorYsusLibHTMX'),
    path('navAutoresConModelFormsetJS/', views.navAutorModelFormsetJS, name='navAutorModelFormsetJS'),
    path('navAutoresConModelFormsetYpaginator/', views.navAutorModelFormsetYpaginator, name='navAutorModelFormsetYpaginator'),
    path('navAutoresYsusLibrosConInlineformset/', views.navAutorYsusLibrosInlienformset, name='navAutorYsusLibrosInlineformset'),
    path('todos-losTitulos-pdf/', views.descargar_pdf, name='descargar_pdf'),
    #Endpoints de la api django rest framework:
    path('api-todosLoslibros/<int:pk>/', views.LibroDetalle.as_view(), name="libro-detail"),
    path('api-todosLoslibros/', views.Libros.as_view(), name="libro-list"),
    path('api-todosLosAutores/', views.Autores.as_view(), name="autor-list"),
    path("", views.api_root),
    path("api-todosLosAutores/<int:pk>/", views.AutorDetalle.as_view(), name="autor-detail"),
    #Creación y actualización de usuarios:
    path('crear-usuario/', views.crear_usuario_inferior, name='crear_usuario'),
    path('usuarios/<str:miembros_de_la_libreria>/', views.UsuariosPorGrupoListView.as_view(), name='lista_usuarios_grupo'),
    # Ruta para actualizar un usuario específico usando su primary key (pk)
    path('usuario/<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='editar_usuario'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
