from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Libro, Autor

# Serializers define the API representation.

class SerializadorLibro(serializers.HyperlinkedModelSerializer):
    autor = serializers.StringRelatedField()
    
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
    )

    class Meta:
        model = Autor
        fields = ["url", "id", "nombre", "apellido", "nacimiento", "muerte", "libros"]
