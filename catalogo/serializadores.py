from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Libro, Autor, Genero, Lenguaje

# Serializers define the API representation.

class SerializadorLibro(serializers.HyperlinkedModelSerializer):
    autor = serializers.HyperlinkedRelatedField(
        many=False, view_name="autor-detail", read_only=True
    )

    lenguaje = serializers.HyperlinkedRelatedField(
        many=False, view_name="lenguaje-detail", read_only=True
    )
    class Meta:
        model = Libro
        fields = [
            "url",
            "id",
            "titulo",
            "autor",
            "descripcion",
            "isbn",
            #"genero",
            "lenguaje"
        ]

        #Asegurarse de que el campo url apunte a la ruta correcta. Se usa para las operaciones c, u, and d de crud:
        extra_kwargs = {
            'url': {'view_name': 'libro-detail', 'format': 'json'}
        }

class SerializadorAutor(serializers.HyperlinkedModelSerializer):
    libros = serializers.HyperlinkedRelatedField(
        many=True, view_name="libro-detail", read_only=True
    )

    def get_url(self, obj, view_name, request, format):
        if obj is None:
            return None # Retorna nulo en lugar de intentar generar la URL sin pk
        return super().get_url(obj, view_name, request, format)

    class Meta:
        model = Autor
        fields = ["url", "id", "nombre", "apellido", "nacimiento", "muerte", "libros"]
        #Asegurarse de que el campo url apunte a la ruta correcta. Se usa para las operaciones c, u, and d de crud:
        extra_kwargs = {
            'url': {'view_name': 'autor-detail', 'format': 'json'}
        }

class SerializadorGenero(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genero
        fields = ['id', 'nombre']

class SerializadorLenguaje(serializers.HyperlinkedModelSerializer):
    libros = serializers.HyperlinkedRelatedField(
        many=True, view_name="libro-detail", read_only=True
    )
    class Meta:
        model = Lenguaje
        fields = ['url', 'id', 'nombre', 'libros']