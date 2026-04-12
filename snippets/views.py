from django.shortcuts import render
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics

# Create your views here.


def inicioSnippets(solicitud):
    """
    Función vista para la página inicio de la app snippets con la lista de todos los snippets.
    """
    # Renderiza la plantilla HTML inicio.html con los datos en la variable contexto
    return render(solicitud,'base1-inicio-snippets.html',context={'listaDeSnippets':SnippetList()})
#Recuerde que podemos colocar el retorno del atributo objects.count() directamente en el valor de la clave del par clave-valor en el diccionario.

from rest_framework import permissions

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

from django.contrib.auth.models import User
from snippets.serializers import UserSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

