from django.db import models
from modules.producto.models import Producto
from modules.auth.models import Usuario

class Inventario(models.Model):
  
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='inventarios',
        verbose_name="Producto",
        help_text="Producto relacionado al movimiento de inventario"
    )
    cantidad = models.PositiveIntegerField(
        verbose_name="Cantidad",
        help_text="Cantidad de productos en el movimiento"
    )
    precio_compra_unitario= models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio de Compra Unitario",
        help_text="Precio de compra por unidad del producto"
    )
    precio_compra_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Precio de Compra Total",
        help_text="Precio total de la compra (cantidad × precio unitario)"
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro",
        help_text="Fecha y hora del registro del inventario"
    )
    estado = models.BooleanField(
        default=True,
        verbose_name="Estado",
        help_text="Estado del movimiento de inventario para el soft delete"
    )
    
    class Meta:
        db_table = 'inventario'
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades - {self.estado}"
    
    def save(self, *args, **kwargs):
        """Calcular precio_compra_total automáticamente"""
        self.precio_compra_total = self.cantidad * self.precio_compra_unitario
        super().save(*args, **kwargs)