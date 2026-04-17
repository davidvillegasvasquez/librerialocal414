from django.urls import path, include
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'snippets' #Creamos el espacio de nombres para acceder desde catalogo.

urlpatterns = [
    path("api/", views.api_root2),
    path("inicio/", views.inicioSnippets, name='irAsnippets'),
    path("", views.SnippetList.as_view(), name="snippet-list"),
    path("<int:pk>/", views.SnippetDetail.as_view(), name="snippet-detail"),
    path("<int:pk>/highlight/", views.SnippetHighlight.as_view(), name="snippet-highlight"),
]
#path("", views.SnippetLista.as_view()), path("", views.api_root),
#Acceder al listado con httpie:
#http GET http://127.0.0.1:8000/snippets/ --unsorted

#Ej de uso de cliente httpie para operaciones crud:

#Agregar registro (agregar recurso):
#http -a david:chacha01 POST http://localhost:8000/snippets/ title="mi primer libro" code="codigo xxyxx-seg" linenos=true language="androidbp" style="abap"

#Borrar registro (borrar recurso):
#http -a david:chacha01 DELETE http://localhost:8000/snippets/4/

urlpatterns += [
    path("snippets/users/", views.UserList.as_view(), name="user-list"),
    path("snippets/users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
