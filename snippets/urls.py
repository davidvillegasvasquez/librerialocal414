from django.urls import path
from snippets import views

#El path vacio para poder hacer la ruta snippets/ que viene de la raíz del proyecto (librerialocal)
urlpatterns = [
    path("", views.snippet_list),
    path("<int:pk>/", views.snippet_detail),
]