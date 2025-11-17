from django import forms
from django.forms import ModelForm
from .models import LibroInstancia, Autor, Libro

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime #for checking renewal date range.

class ModeloFormRenovDeLibros(ModelForm):
    """
    Este es el formulario no consolidado (el que se presenta por primera vez). Se usa principalmente para limpiar y validar la fecha de renovación introducida por el usuario.
    Si solo necesita un formulario para asignar los campos de un solo modelo, entonces su modelo ya definirá la mayor parte de la información que necesita en su formulario: campos, etiquetas, texto de ayuda, etc. En lugar de recrear las definiciones de modelo en su formulario, usando el enfoque de usar un Form y la función view, es más fácil usar una clase auxiliar ModelForm como hacemos aquí, para crear el formulario a partir de su modelo. La gran ventaja de usar ModelForm es que si tiene que usar muchos campos, puede reducir la cantidad de código de manera bastante significativa.
    Ahora, en formularios raros muy complejos, no genéricos con uso de multiples modelos, usamos el enfoque Form-función view.
    """
    def clean_debidoderegresar(self):
        fecha = self.cleaned_data['debidoderegresar']
        #Nota para el enfoque ModelForm (el que estamos usando): la propiedad método debe llamarse como nombre reservado django, clean_nombredelcampoenelmodelo,
#en este caso, clean_debidoderegresar, y el self.cleaned_data['nombredelcampoenelmodelo'], es decir, self.cleaned_data['debidoderegresar'] tanto aquí como en su vista respectiva, renovacionLibroPorLibrero.

        if fecha < datetime.date.today():
            raise ValidationError(_('Fecha inválida - renovación al pasado!!!'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if fecha > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Fecha inválida - renovación más allá de las 4 semanas'))

        # Remember to always return the cleaned fecha.
        return fecha

    class Meta:
        model = LibroInstancia
        #Configuramos los campos del modelo que vamos a utilizar:
        fields = ['debidoderegresar',]
        labels = { 'debidoderegresar': _('Fecha de renovación'), }
        help_texts = { 'debidoderegresar': _('Introduzca una fecha entre ahora y 4 semanas arriba (lo normal son 3).'), }
        #Para hacer un widget de introducción de fecha tipo calendario sólo de selección, usamos forms.DateInput con los atributos type en date y onkeydown en return false:
        widgets = {'debidoderegresar': forms.DateInput(attrs={'type': 'date', 'onkeydown': 'return false', 'placeholder': 'YYYY-MM-DD'}),}


class LibroConsultaForm(forms.Form):
    # Campo para la selección de la categoría (relacionada con Categoria)
    autorEnFormulario = forms.ModelChoiceField(queryset=Autor.objects.all(), widget=forms.Select(attrs={}), required=False)

    # Campo para el nombre del producto (relacionado con Producto)
    librosEnFormulario = forms.ModelChoiceField(queryset=Libro.objects.none(), widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_librosEnFormulario'}), label="Sus libros",required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Almacena el queryset del segundo campo
        self.fields['librosEnFormulario'].queryset = Libro.objects.none()
        if 'autorEnFormulario' in self.data:
            try:
                autorSeleccionadoEnModelChoiceField = self.data.get('autorEnFormulario')
                
                self.fields['librosEnFormulario'].queryset = Libro.objects.all().filter(autor=autorSeleccionadoEnModelChoiceField) # Usa el nombre de tu campo de relación
                print(f"valor de self.fields['librosEnFormulario'].queryset: {self.fields['librosEnFormulario'].queryset}")
            except (ValueError, TypeError):
                pass # No se hace nada si no hay objeto_principal o no es válido
