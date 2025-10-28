from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registroUsuario/', views.registrar_usuario, name='registrar-usuario'),

]
