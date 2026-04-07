"""librerialocal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [path('admin/', admin.site.urls),]

urlpatterns += [path('catalogo/', include('catalogo.urls')),]

urlpatterns += [path('snippets/', include('snippets.urls')),]

urlpatterns += [path('', RedirectView.as_view(url='/catalogo/', permanent=True)),]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')), path('', RedirectView.as_view(url='/accounts/', permanent=True)),
]
#El nombre url accounts no puede ser arbitrario, porque django en sus vistas genéricas utiliza este nombre en su implementación.

#urls de la api rest:

from catalogo.views import VistaConjuntoDeUsuarios, VistaConjuntoDeGrupos, LibrosDeGallegos, LibsDeRangel #views
from rest_framework import routers

enrutador = routers.DefaultRouter()
enrutador.register(r"users", VistaConjuntoDeUsuarios)
enrutador.register(r"groups", VistaConjuntoDeGrupos)
enrutador.register(r"romulo-gallegos", LibrosDeGallegos)
enrutador.register(r"carlos-rangel", LibsDeRangel, basename='carlos-rangel') #Hay que usar el parámetro basename porque estoy serializando el mismo modelo más de una vez.

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    path("", include(enrutador.urls)),
    path("api-auth-cualquiervaina/", include("rest_framework.urls", namespace="rest_framework")),
]

