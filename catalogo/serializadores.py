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
    #Así serializamos un campo con relación ManyToMany:
    genero = serializers.HyperlinkedRelatedField(
        many=True, 
        view_name="genero-detail", 
        read_only=True,
        #queryset=Genero.objects.all()
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
            "genero",
            "lenguaje"
        ]

        #Asegurarse de que el campo url apunte a la ruta correcta. Se usa para las operaciones c, u, and d de crud:
        extra_kwargs = {
            'url': {'view_name': 'libro-detail', 'format': 'json'}
        }
    """
    def create(self, validated_data):
        # 1. Extraemos los campo de los datos validados
        autor_data = validated_data.pop('autor_id', None)
        lenguaje_data = validated_data.pop('lenguaje_id', None)
        generos_data = validated_data.pop('genero_id', [])

        # 2. Creamos la instancia del libro principal
        libro = Libro.objects.create(**validated_data)

        # 3. Guardamos/vinculamos las relaciones muchos a muchos manualmente
        for gen in generos_data:
            libro.genero.add(gen)

        # 4. Retornamos la instancia creada
        return libro        
    """                
class SerializadorAutor(serializers.HyperlinkedModelSerializer):
    libro = serializers.HyperlinkedRelatedField(
        many=True, view_name="libro-detail", read_only=True
    )

    def get_url(self, obj, view_name, request, format):
        if obj is None:
            return None # Retorna nulo en lugar de intentar generar la URL sin pk
        return super().get_url(obj, view_name, request, format)

    class Meta:
        model = Autor
        fields = ["url", "id", "nombre", "apellido", "nacimiento", "muerte", "libro"]
        #Asegurarse de que el campo url apunte a la ruta correcta. Se usa para las operaciones c, u, and d de crud:
        extra_kwargs = {
            'url': {'view_name': 'autor-detail', 'format': 'json'}
        }


class SerializadorGenero(serializers.HyperlinkedModelSerializer):
    libro = serializers.HyperlinkedRelatedField(
        many=True, view_name="libro-detail", read_only=True
    )

    class Meta:
        model = Genero
        fields = ['url', 'id', 'nombre', 'libro']

class SerializadorLenguaje(serializers.HyperlinkedModelSerializer):
    libro = serializers.HyperlinkedRelatedField(
        many=True, view_name="libro-detail", read_only=True
    )
    class Meta:
        model = Lenguaje
        fields = ['url', 'id', 'nombre', 'libro']
