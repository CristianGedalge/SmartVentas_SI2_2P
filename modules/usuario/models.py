from django.db import models
from modules.auth.models import Usuario

# Create your models here.

class UsuarioInfo(models.Model):
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='info',
        verbose_name="Usuario"
    )
    url_img = models.CharField(max_length=255,null=True, verbose_name="Url_Img")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    estado = models.BooleanField(default=True, verbose_name="Estado activo")

    
    class Meta:
        db_table = 'usuario_info'
        verbose_name = "Información de Usuario"
        verbose_name_plural = "Información de Usuarios"
        ordering = ['apellido', 'nombre']
        
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.usuario.email})"
    
    @property
    def nombre_completo(self):
        """Devuelve el nombre completo"""
        return f"{self.nombre} {self.apellido}".strip()
    
    @property
    def email(self):
        """Acceso rápido al email del usuario"""
        return self.usuario.email
    
    def save(self, *args, **kwargs):
        # Convertir nombre y apellido a formato título
        self.nombre = self.nombre.title()
        self.apellido = self.apellido.title()
        
        # Limpiar teléfono (solo números, espacios y guiones)
        if self.telefono:
            import re
            self.telefono = re.sub(r'[^\d\s\-\+\(\)]', '', self.telefono)
        
        super().save(*args, **kwargs)