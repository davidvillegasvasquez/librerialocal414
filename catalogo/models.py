# Create your models here.

from django.db import models
from django.conf import settings
from datetime import date
from io import BytesIO
import qrcode
from django.core.files.base import ContentFile


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

    class Meta:
        ordering = ['id']

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Libro(models.Model):
    """
    Modelo que representa un libro (pero no un Ejemplar específico).
    """
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True, related_name="librosx") #Atributo related_name para los hipervínculos de la api rest. Note que usamos un nombre arbitrario que no tiene nada con los campos de los modelos en cuestión.
#Averiguar porque no es obligatorio usar related_name para los demás serializadores. Creo que es porque Autor se definió con el atributo método get_absolute_url.
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
from django.conf import settings

class LibroInstancia(models.Model):
    """
    Modelo que representa una copia específica de un libro (i.e. que puede ser prestado por la biblioteca).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    libro = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True)
    imprenta = models.CharField(max_length=200)
    debidoderegresar = models.DateField(null=True, blank=True)
    #En la definición de modelos no usamos from django.contrib.auth import get_user_model para obtener el modelo de usuario que ha sido personalizado, sino que lo traemos desde setting:
    prestatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    #Foto portada:
    portada = models.ImageField(upload_to='fotos_portada/', blank=True, null=True)
    imgqr = models.ImageField(upload_to='fotos_qr/', blank=True, null=True)

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

    #Tenemos que sobreescribir el método save en vez del form_valid en la vista CrearLibroInstancia xq a pesar de que se puede crear el qr sin ningún problema,
 #no se podrá actualizar puesto que el cambio no se persiste cuando llamemos la vista ActualizarLibroInstancia; los datos limpios del formulario aún no están consolidados en la instancia cuándo se ejecute la vista:
    def save(self, *args, **kwargs):
        # Generar el texto a partir de los campos. Construir la estructura de datos en formato vCard
        vcard_data = (
            "BEGIN:VCARD\n"
            "VERSION:3.0\n"
            f"ID:{self.id}\n" #Se crea automáticamente (default=uuid.uuid4 en la definición del campo en el modelo).
            f"TITULO:{self.libro}\n"
            f"IMPRENTA:{self.imprenta}\n"
            "END:VCARD"
        )

        #Generar la imagen en formato png del código QR con qrcode. No lo haremos con portada, por lo cual la foto de de portada se guardará en el formato que la ingresemos:
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(vcard_data)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        
        # 4. Guardar las imagenes en búfer de formato PNG
        buffer_imgqr = BytesIO()
        img_qr.save(buffer_imgqr, format="PNG")
        file_name_qr = f"qr_{self.libro}.png"
        # 5. Asignar el archivo al campo ImageField usando ContentFile
        self.imgqr.save(file_name_qr, ContentFile(buffer_imgqr.getvalue()), save=False)
        super().save(*args, **kwargs)


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
        ordering = ['id']

class Lenguaje(models.Model):
    """
    Modelo que representa el lenguaje
    """
    nombre = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        """
        String que representa al objeto Lenguaje
        """
    
        return self.nombre

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    creador = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='usuarios_creados'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
