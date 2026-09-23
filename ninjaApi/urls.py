from django.urls import path
#from django.contrib import admin #Aunque no se vé el uso del admin aquí, si no lo importo se presenta la excepción "LookupError: No installed app with label 'admin'".
from catalogo.models import *

urlpatterns = [
    #path('', views.inicio, name='vistaHome'), 
    #path('url-x/', views.vistaX.as_view(), name='cualquiervaina'),
]


