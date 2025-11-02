from django.db import models
from django.core.exceptions import ValidationError
from modules.categoria.models import Categoria
from modules.marca.models import Marca
class Producto(models.Model):
    
    categoria = models.ForeignKey(
        Categoria,
        null=True,on_delete=models.CASCADE, related_name='productos',
        verbose_name="Categoría",
        help_text="Categoría a la que pertenece el producto")
    
    marca = models.ForeignKey(
        Marca,
        null=True,on_delete=models.CASCADE, related_name='productos',
        verbose_name="MArca",
        help_text="marca a la que pertenece el producto")
    
    nombre = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="Nombre del Producto", 
        help_text="Nombre del producto"
    )
    descripcion = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Descripción",  
        help_text="Descripción detallada del producto"
    )
    url_img = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Url de imagen",  
        help_text="Url de la imagen del producto"
    )
    precio = models.DecimalField(
        default=0.00,
        max_digits=10, 
        decimal_places=2,
        verbose_name="Precio",  
        help_text="Precio de venta del producto"
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock Disponible", 
        help_text="Cantidad disponible en inventario"
    )
    estado = models.BooleanField(
        default=True,
        verbose_name="Estado Activo",  
        help_text="True: Activo, False: Inactivo"
    )
    tiempo_garantia = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Meses de Garantía",
        help_text="Duración de la garantía en meses (ej: 12, 24, 36)"
    )
    tipo_garantia = models.CharField(
    max_length=50,
    blank=True,
    choices=[
        ('FABRICANTE', 'Garantía del Fabricante'),
        ('TIENDA', 'Garantía de la Tienda'),
        ('NINGUNO', 'Sin Garantía'),
    ],
    default='NINGUNO',  
    verbose_name="Tipo de Garantía",
    help_text="Tipo de garantía que ofrece el producto"
    )

    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",  
        help_text="Fecha de creación del producto"
    )
    
    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-fecha']  # Más recientes primero
    
    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock})"
    
    def esta_disponible(self):
        """Verifica si el producto está disponible (activo y con stock)"""
        return self.estado and self.stock > 0
    
    def reducir_stock(self, cantidad):
        """Reduce el stock del producto"""
        if self.stock >= cantidad:
            self.stock -= cantidad
            self.save()
            return True
        return False
    
    def aumentar_stock(self, cantidad):
        """Aumenta el stock del producto"""
        self.stock += cantidad
        self.save()
