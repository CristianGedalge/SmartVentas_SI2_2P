from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def login(request):
    """Vista de prueba para login que muestra un mensaje de logueado"""
    return JsonResponse({
        'status': 'success',
        'message': 'Usuario logueado correctamente',
        'data': {
            'user': 'usuario_prueba',
            'timestamp': '2025-10-22'
        }
    })
