from django.db import models

# Create your models here.

class Categoria(models.Model):

    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categoria'

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Convertir nombre a formato título antes de guardar
        if self.nombre:
            self.nombre = self.nombre.title()
        super().save(*args, **kwargs)

