from django.urls import path
from . import views

# URLs para el módulo de marcaa
urlpatterns = [
    path('createMarca/', views.crear_marca, name='crear-marca'),
    
    path('findAllMarca/', views.listar_marca, name='listar-marca'),
    
    path('updateMarca/<int:id>/', views.actualizar_marca, name='actualizar-marca'),

    path('deleteMarca/<int:id>/', views.eliminar_marca, name='eliminar-marca'),

]