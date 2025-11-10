import uuid
from django.db import models
from django.utils import timezone
from modules.usuario.models import Usuario  
from modules.producto.models import Producto
from modules.descuento.models import Descuento

class Venta(models.Model):
    codigo_venta = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ventas')
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    metodo_pago = models.CharField(max_length=50, default='STRIPE')
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'venta'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha']  # Más recientes primero

    def save(self, *args, **kwargs):
        if not self.codigo_venta:
            # genera un código tipo VNT-20251102-AB12
            self.codigo_venta = f"VNT-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo_venta} - {self.usuario.email}"


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_aplicado = models.ForeignKey(
        Descuento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ventas_aplicadas',
        help_text="Descuento que se aplicó en el momento de la venta"
    )
    porcentaje_descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Porcentaje de descuento aplicado (ej: 15.50)"
    )
    monto_descuento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Monto total de descuento aplicado"
    )

    class Meta:
        db_table = 'detalle_venta'
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalles de Ventas'