from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Libro, Autor

# Serializers define the API representation.

class SerializadorLibro(serializers.HyperlinkedModelSerializer):
    autor = serializers.HyperlinkedRelatedField(
        many=False, view_name="autor-detail", read_only=True
    ) #many=False: un libro - un autor.
    class Meta:
        model = Libro
        fields = [
            "url",
            "id",
            "titulo",
            "autor",
            "descripcion",
            "isbn",
        ]
class SerializadorAutor(serializers.HyperlinkedModelSerializer):
    libros = serializers.HyperlinkedRelatedField(
        many=True, view_name="libro-detail", read_only=True
    ) #many=True: un autor - varios libros.

    class Meta:
        model = Autor
        fields = ["url", "id", "nombre", "apellido", "nacimiento", "muerte", "libros"]
