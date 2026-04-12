from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

#El path vacio para poder hacer la ruta snippets/ que viene de la raíz del proyecto (librerialocal)

app_name = 'snippets' #Creamos el espacio de nombres para acceder desde catalogo.

urlpatterns = [
    path("", views.inicioSnippets, name='irAsnippets'), 
    path("<int:pk>/", views.SnippetDetail.as_view()),
]
#Agreguemos la url para ver la vista en conjunto de la lista de snippets serializados con el cliente httpie o con el cliente drf, o para operaciones crud con el cliente httpie:
urlpatterns += [
    path("snippet-list-httpie/", views.SnippetList.as_view()),
]
#Acceder al listado con httpie:
#http GET http://127.0.0.1:8000/snippets/snippet-list-httpie/ --unsorted

#Ej de uso de cliente httpie para operaciones crud:

#Agregar registro (agregar recurso):
#http -a david:chacha01 POST http://localhost:8000/snippets/snippet-list-httpie/ title="mi primer libro" code="codigo xxyxx-seg" linenos=true language="androidbp" style="abap"

#Borrar registro (borrar recurso):
#http -a david:chacha01 DELETE http://localhost:8000/snippets/41/

urlpatterns += [
    path("users/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
