#Cliente drf para la vista de serializador, LibrosDeGallego.
#Ejecutar en la shell django con: exec(open('y.py').read())
from catalogo.serializadores import SerializarLibros
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from catalogo.views import LibrosDeGallegos


GallegosViewsets_ModelViewSet = LibrosDeGallegos()

print(f'GallegosViewsets_ModelViewSet.queryset: {GallegosViewsets_ModelViewSet.queryset}')
print(f'GallegosViewsets_ModelViewSet.get_queryset(): {GallegosViewsets_ModelViewSet.get_queryset()}')
print(f"GallegosViewsets_ModelViewSet.queryset.values('titulo', 'id', 'isbn'): {GallegosViewsets_ModelViewSet.queryset.values('titulo', 'id', 'isbn')}")

"""
for obj in GallegosViewsets_ModelViewSet.queryset:
    print(obj.__dict__)
"""

