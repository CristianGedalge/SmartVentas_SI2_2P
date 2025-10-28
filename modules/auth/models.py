from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from modules.roles.models import Rol
class Usuario(models.Model): 
    rol = models.ForeignKey(Rol, on_delete = models.PROTECT)
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    password = models.CharField(max_length=128, verbose_name="Contraseña")
    estado = models.BooleanField(default=True, verbose_name="Estado activo")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    
    class Meta:
        db_table = 'usuario'
        
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Hashear la contraseña solo si es nueva o ha cambiado
        if self.pk is None or 'password' in kwargs.get('update_fields', []):
            if not self.password.startswith('pbkdf2_'):  # No hashear si ya está hasheada
                self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def check_password(self, raw_password):
        """Verificar contraseña"""
        return check_password(raw_password, self.password)
    
    def set_password(self, raw_password):
        """Establecer nueva contraseña"""
        self.password = make_password(raw_password)