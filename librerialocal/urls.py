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

urlpatterns += [path('', RedirectView.as_view(url='/catalogo/', permanent=True)),]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')), path('', RedirectView.as_view(url='/accounts/', permanent=True)),
]
#El nombre url accounts no puede ser arbitrario, porque django en sus vistas genéricas utiliza este nombre en su implementación.

#urls para la api navegable de drf. No es obligatorio pero es conveniente construir una para usar la api navegable con fines de agilizar para pruebas manuales en desarrollo. Consultar en la documentación de drf:

urlpatterns += [
    path("entraraladrf/", include("rest_framework.urls")),
]
#Por supuesto, 'entrarAlaDrf/' parte del patrón puede ser cualquier URL que desees utilizar (nombre arbitrario). Para usarla se debe acompañar con la acción a ejecutar, ej: http://127.0.0.1:8000/entraraladrf/login/

#Urls para los JWT:
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# urls para dj_rest_auth:
urlpatterns += [
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]

