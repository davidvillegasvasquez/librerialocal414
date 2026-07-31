from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Libro, Autor, Genero, Lenguaje

# Serializers define the API representation.

class SerializadorLibro(serializers.HyperlinkedModelSerializer):
    autor = serializers.HyperlinkedRelatedField(
        many=False, view_name="autor-detail", read_only=False, queryset=Autor.objects.all()
    )

    lenguaje = serializers.HyperlinkedRelatedField(
        many=False, view_name="lenguaje-detail", read_only=False, queryset=Lenguaje.objects.all()
    )
    #Así serializamos un campo con relación ManyToMany:
    genero = serializers.HyperlinkedRelatedField(
        many=True, 
        view_name="genero-detail", 
        read_only=False, #Porque se necesita para las operaciones updates.
        queryset=Genero.objects.all()
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
                   
class SerializadorAutor(serializers.HyperlinkedModelSerializer):
    #Creamos un campo auxiliar para extraer los libros del autor usando libro-detail y acceder a ellos por medio de dicho campo auxiliar. 
#Aquí es librosx, el nombre arbitrario que definimos como related_name en el modelo Autor:
    librosx = serializers.HyperlinkedRelatedField(
        many=True, view_name="libro-detail", read_only=True
    )
    
    class Meta:
        model = Autor
        fields = ["url", "id", "nombre", "apellido", "nacimiento", "muerte", "librosx"]
        #Asegurarse de que el campo url apunte a la ruta correcta. Se usa para las operaciones c, u, and d de crud:
        extra_kwargs = {
            'url': {'view_name': 'autor-detail', 'format': 'json'}
        }


class SerializadorGenero(serializers.HyperlinkedModelSerializer):
    titulo = serializers.HyperlinkedRelatedField(
        many=True, view_name="libro-detail", read_only=True
    )

    class Meta:
        model = Genero
        fields = ['url', 'id', 'nombre', 'titulo']

class SerializadorLenguaje(serializers.HyperlinkedModelSerializer):
    titulo = serializers.HyperlinkedRelatedField(
        many=True, view_name="libro-detail", read_only=True
    )
    class Meta:
        model = Lenguaje
        fields = ['url', 'id', 'nombre', 'titulo']
