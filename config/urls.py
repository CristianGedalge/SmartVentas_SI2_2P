"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework import permissions


from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración de Swagger

schema_view = get_schema_view(
   openapi.Info(
      title="SmartVentas API",
      default_version='v1',
      description="API para el sistema de SmartVentas",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@smartventas.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    #api
    path('api/auth/', include('modules.auth.urls')),
    path('api/rol/', include('modules.roles.urls')),
    path('api/categoria/', include('modules.categoria.urls')),
    path('api/bitacora/', include('modules.bitacora.urls')),
    path('api/marca/', include('modules.marca.urls')),
    path('api/usuario/', include('modules.usuario.urls')),
    path('api/producto/', include('modules.producto.urls')),
    path('api/inventario/', include('modules.inventario.urls')),
    path('api/descuento/', include('modules.descuento.urls')),
    path('api/venta/', include('modules.venta.urls')),
    path('api/reporte/', include('modules.reporte.urls')),
    #Swagger
    # Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 
]
