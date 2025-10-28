from django.db import models

# Create your models here.

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre del rol")
    estado = models.BooleanField(default=True, verbose_name="Estado activo")
    fecha_registro  = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    
    class Meta:
        db_table = 'rol'
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ['nombre']
        
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Convertir nombre a formato título
        self.nombre = self.nombre.title()
        super().save(*args, **kwargs)
    
    @property
    def usuarios_count(self):
        """Contar cuántos usuarios tienen este rol"""
        return self.usuarios.filter(estado=True).count()
    

class Permiso(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del permiso")
    class Meta:
        db_table = 'permiso'
        verbose_name = "Permiso"
        verbose_name_plural = "Permisos"
        ordering = ['nombre']
        
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Convertir nombre a formato título
        self.nombre = self.nombre.title()
        super().save(*args, **kwargs)
    

class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='rol_permisos')
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE, related_name='rol_permisos')
    estado = models.BooleanField(default=False, verbose_name="Estado activo")
    class Meta:
        db_table = 'rol_permiso'
        verbose_name = "Rol Permiso"
        verbose_name_plural = "Roles Permisos"
        unique_together = ('rol', 'permiso')  # Evitar duplicados
        ordering = ['rol__nombre', 'permiso__nombre']
        
    def __str__(self):
        return f"{self.rol.nombre} - {self.permiso.nombre}"