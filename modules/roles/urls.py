from django.urls import path
from . import views

# URLs para el módulo de roles
urlpatterns = [
    path('createRol/', views.crear_rol, name='crear-rol'),
    
    path('findAllRoles/', views.listar_roles, name='listar-roles'),
    
    path('updateRol/<int:id>/', views.actualizar_rol, name='actualizar-parcial-rol'),

    path('deleteRol/<int:id>/', views.eliminar_rol, name='eliminar-rol'),
    
    #Permisos
    path('createPermiso/', views.crear_permiso, name='crear-permiso'),
    
    path('permisosXRol/<int:id>/', views.listar_permisosXRol, name='listar-permisos-XRol'),
    path('actualizarPermisosRol/<int:id>/', views.actualizar_permisos_rol, name='actualizar-permisos-rol'),  
    # path('permisos/<int:pk>/', views.obtener_permiso, name='obtener-permiso'),
    
    # ========== GESTIÓN ROL-PERMISO (cuando los agregues) ==========
    # path('rol-permiso/asignar/', views.asignar_permiso, name='asignar-permiso'),
    # path('rol-permiso/quitar/<int:rol_id>/<int:permiso_id>/', views.quitar_permiso, name='quitar-permiso'),
]