from django.db import models
from modules.auth.models import Usuario

class Bitacora(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    accion = models.TextField(verbose_name="Acción")
    ip = models.GenericIPAddressField(verbose_name="Dirección IP",null=True,blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de registro")
    
    class Meta:
        db_table = 'bitacora'
        verbose_name = "Bitácora"
        verbose_name_plural = "Bitácoras"
        ordering = ['-fecha_registro']  # Más recientes primero
    
    def __str__(self):
        return f"{self.usuario.email} - {self.accion} - {self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')}"