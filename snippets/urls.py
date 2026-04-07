from django.urls import path
from snippets import views

#El path vacio para poder hacer la ruta snippets/ que viene de la raíz del proyecto (librerialocal)

app_name = 'snippets'

urlpatterns = [
    path("", views.inicioSnippets, name='irAsnippets'),
    path("<int:pk>/", views.snippet_detail),
]