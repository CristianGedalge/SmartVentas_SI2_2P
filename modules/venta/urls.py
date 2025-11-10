from django.urls import path
from . import views

# URLs para el módulo de venta
urlpatterns = [

    path('prepararVenta/', views.preparar_venta, name='preparar-venta'),

    path('createVenta/', views.registrar_venta, name='crear-venta'),

    path('misVentas/', views.mis_ventas, name='mis-ventas'),
]