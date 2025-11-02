from django.db import models
from modules.producto.models import Producto
from modules.categoria.models import Categoria

class Descuento(models.Model):
    
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='descuentos',
        verbose_name="Producto",
        help_text="Producto específico (solo si tipo_aplicacion es PRODUCTO)"
    )
    porcentaje = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor del Descuento",
        help_text="Porcentaje (ej: 15.00) o monto fijo (ej: 50.00)"
    )

    fecha_inicio = models.DateTimeField(
        verbose_name="Fecha de Inicio",
        help_text="Fecha y hora de inicio del descuento"
    )
    fecha_fin = models.DateTimeField(
        verbose_name="Fecha de Fin",
        help_text="Fecha y hora de finalización del descuento"
    )
    estado = models.BooleanField(
        default=True,
        verbose_name="Estado Activo",
        help_text="True: Activo, False: Inactivo"
    )
    
    class Meta:
        db_table = 'descuento'
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuentos'
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.nombre} - {self.valor}{'%' if self.tipo_descuento == 'PORCENTAJE' else ' Bs.'}"
    
    def esta_vigente(self):
        """Verifica si el descuento está vigente"""
        from django.utils import timezone
        ahora = timezone.now()
        return self.estado and self.fecha_inicio <= ahora <= self.fecha_fin
    
    def calcular_descuento(self, precio_original):
        """Calcula el monto de descuento según el tipo"""
        if self.tipo_descuento == 'PORCENTAJE':
            return (precio_original * self.valor) / 100
        else:  # MONTO_FIJO
            return self.valor
    
    def precio_con_descuento(self, precio_original):
        """Calcula el precio final con descuento aplicado"""
        descuento = self.calcular_descuento(precio_original)
        precio_final = precio_original - descuento
        return max(precio_final, 0)  # No puede ser negativo
    