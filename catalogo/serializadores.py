from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Libro, Autor

# Serializers define the API representation.
class SerializarUsuarios(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]

class SerializarGrupos(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]

class SerializarLibros(serializers.ModelSerializer):
    # Usamos StringRelatedField para mostrar el nombre del autor en lugar de su ID
    autor = serializers.StringRelatedField()

    class Meta:
        model = Libro
        fields = ['titulo', 'isbn', 'autor']
