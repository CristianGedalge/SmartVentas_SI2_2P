from django.urls import path
from . import views

# URLs para el módulo de venta
urlpatterns = [

    path('prepararVenta/', views.preparar_venta, name='preparar-venta'),

    path('createVenta/', views.registrar_venta, name='crear-venta'),

    path('misVentas/', views.mis_ventas, name='mis-ventas'),

    path('descargar-nota/<int:id>/', views.descargar_nota_venta, name='descargar_nota_venta'),
]