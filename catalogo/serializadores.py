from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Libro, Autor

# Serializers define the API representation.

class SerializadorLibro(serializers.HyperlinkedModelSerializer):
    autor = serializers.HyperlinkedRelatedField(
        many=False, view_name="autor-detail", queryset=Autor.objects.all())
    #id = serializers.IntegerField(required=False) #Para poder visualizarlo en el renderizado.

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
        extra_kwargs = {
        'Autor': {'view_name': 'autor-detail'}
    }

class SerializadorAutor(serializers.HyperlinkedModelSerializer):
    libros = serializers.HyperlinkedRelatedField(
        many=True, view_name="libro-detail", read_only=True
    ) #many=True: un autor - varios libros.
    
    #id = serializers.IntegerField(read_only=True, style={'base_template': 'catalogo/autor_list.html'})

    class Meta:
        model = Autor
        fields = ["url", "id", "nombre", "apellido", "nacimiento", "muerte", "libros"]

