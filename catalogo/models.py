# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.

class Genero(models.Model):
    """
    Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.).
    """
    nombre = models.CharField(max_length=200, help_text="Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.)")

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return self.nombre

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Libro(models.Model):
    """
    Modelo que representa un libro (pero no un Ejemplar específico).
    """
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genero = models.ManyToManyField(Genero, help_text="Seleccione un genero para este libro")
    lenguaje = models.ForeignKey('Lenguaje', on_delete=models.SET_NULL, null=True)
   
    def __str__(self):
        """
        String que representa al objeto Libro usando su atributo titulo.
        """
        return self.titulo
#El método get_absolute_url para usarlo en las plantillas como href="{{ objeto.get_absolute_url }}", es generalmente preferible porque crea dinamicamente URLs más genéricas y fáciles de mantener en el código del modelo,
#mientras que la etiqueta {% url 'nombreRefDelaUrlEnPath' objeto.id %} es una forma directa de usar estas URLs dentro de las plantillas. get_absolute_url() se enfoca en la lógica de la URL en
#el modelo y es esencial para la integración con la aplicación de administración de Django y la generación de enlaces absolutos:
    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        """
        return reverse('detallesDeLibro', args=[str(self.id)])

    class Meta:
        ordering = ['titulo', 'autor']

    def mostrar_genero(self):
    #Creates a string for tre in Admin.
        return ', '.join([ genero.nombre for genero in self.genero.all()[:3] ]) 

    mostrar_genero.short_description = 'Genero'

import uuid # Requerida para las instancias de libros únicos
from django.core.validators import MaxValueValidator, MinValueValidator 

class LibroInstancia(models.Model):
    """
    Modelo que representa una copia específica de un libro (i.e. que puede ser prestado por la biblioteca).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    libro = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True)
    imprenta = models.CharField(max_length=200)
    debidoderegresar = models.DateField(null=True, blank=True)
    prestatario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    PRESTAMO_STATUS = (
        ('m', 'Mantenimieno'),
        ('p', 'En prestamo'),
        ('d', 'Disponible'),
        ('r', 'Reservado'),
    )

    estatus = models.CharField(max_length=1, choices=PRESTAMO_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')

    class Meta:
        ordering = ["debidoderegresar"] #ordering es un apuntador-identificador de palabra reservada de django para esta clase, no puedo usar el nombre "ordenar".
        permissions = (("puedeMarcarRetornado", "Tiene permiso para marcar libro como retornado"),)

    @property
    def estaVencido(self):
        if self.debidoderegresar and date.today() > self.debidoderegresar:
            return True
        return False

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        #return '%s (%s)' % (self.id,self.libro.titulo)
        return f'{self.id} ({self.libro.titulo})' #Usando el formateo de cadena a partir de python 3.6

class Autor(models.Model):
    """
    Modelo que representa un autor
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nacimiento = models.DateField(null=True, blank=True)
    muerte = models.DateField('Muerte', null=True, blank=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('autorDetalles', args=[str(self.id)]) 

    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return '%s, %s' % (self.apellido, self.nombre)

    class Meta:
        ordering = ['apellido']

class Lenguaje(models.Model):
    """
    Modelo que representa el lenguaje
    """
    nombre = models.CharField(max_length=100)

    def __str__(self):
        """
        String que representa al objeto Lenguaje
        """
        return self.nombre
