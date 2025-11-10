from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from decimal import Decimal
from modules.producto.models import Producto
from .models import Venta, DetalleVenta
from modules.auth.utils import permiso_requerido

from .serializers import VentaSerializer

from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa  # pip install pdfkit
import stripe
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


@api_view(['POST'])
@permiso_requerido(None)
def preparar_venta(request):
    cliente = request.usuario
    items_data = request.data.get("items", [])
    total = Decimal("0.00")

    for p in items_data:
        producto = get_object_or_404(Producto, id=p["producto_id"])
        cantidad = int(p.get("cantidad", 1))
        descuento = producto.descuentos.filter(
            estado=True,
            fecha_inicio__lte=timezone.now(),
            fecha_fin__gte=timezone.now()
        ).first()
        descuento_valor = Decimal("0.00")
        precio_unitario = producto.precio
        if descuento:
            descuento_valor = (precio_unitario * descuento.porcentaje / 100).quantize(Decimal("0.01"))
        subtotal = (precio_unitario - descuento_valor) * cantidad
        total += subtotal

    payment_intent = stripe.PaymentIntent.create(
        amount=int(total * 100),
        currency="usd"
    )

    return Response({
        "total": str(total),
        "stripe_client_secret": payment_intent["client_secret"],
        "stripe_payment_intent_id": payment_intent["id"] 
    })


@api_view(['POST'])
@permiso_requerido(None)
def registrar_venta(request):
    """
    Registra una venta con Stripe como método de pago.
    Recibe un JSON como:
    {
        "cliente_id": 1,
        "productos": [
            {"producto_id": 5, "cantidad": 2},
            {"producto_id": 4, "cantidad": 1}
        ]
    }
    """
    cliente =request.usuario;
    items_data = request.data.get("items", [])
    payment_intent_id = request.data.get("payment_intent_id")
    print(len(items_data),'logitud de items')
    if not cliente or not items_data or not payment_intent_id:
        return Response({"error": "Datos incompletos."}, status=status.HTTP_400_BAD_REQUEST)


    # Verificar el pago en Stripe
    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    # if payment_intent.status != 'succeeded':
    #     return Response({"error": "El pago no fue exitoso."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Crear venta
    venta = Venta.objects.create(cliente=cliente)

    total = Decimal("0.00")

    # Procesar productos
    for p in items_data:
        producto = get_object_or_404(Producto, id=p["producto_id"])
        cantidad = int(p.get("cantidad", 1))
        print( cantidad)

        #Verificar descuento activo
        descuento = producto.descuentos.filter(
            estado=True,
            fecha_inicio__lte=timezone.now(),
            fecha_fin__gte=timezone.now()
        ).first()
        descuento_valor = Decimal("0.00")
        precio_unitario = producto.precio
        if descuento:
            descuento_valor = (precio_unitario * descuento.porcentaje / 100).quantize(Decimal("0.01"))

        subtotal = (precio_unitario - descuento_valor) * cantidad
        total += subtotal
        # Registrar detalle
        detalle = DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal,
            descuento_aplicado=descuento,# el obj descuento
            porcentaje_descuento=descuento.porcentaje if descuento else Decimal("0.00"),
            monto_descuento=descuento_valor * cantidad
        )
        producto.reducir_stock(cantidad)

    #     # Generar garantía si aplica
    #     if producto.tipo_garantia == "TIENDA":
    #         Garantia.objects.create(
    #             detalle_venta=detalle,
    #             tipo_garantia=producto.tipo_garantia
    #         )


        # Reducir stock
        producto.reducir_stock(cantidad)

    # Guardar total y stripe_id
    venta.total = total
    # venta.stripe_payment_intent = payment_intent["id"]
    venta.save()

    return Response({
        "venta_id": venta.id,
        "total": str(total),
        "mensaje": "Venta registrada."
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permiso_requerido(None)
def mis_ventas(request):
    """
    Lista todas las ventas del usuario autenticado.
    """
    ventas = Venta.objects.filter(cliente=request.usuario).order_by('-fecha')
    serializer = VentaSerializer(ventas, many=True)
    return Response(serializer.data)





@api_view(['GET'])
@permiso_requerido(None)
def descargar_nota_venta(request, id):
    """
    Descarga la nota de venta/factura en PDF.
    """
    venta = get_object_or_404(Venta, id=id)
    html_string = render_to_string('nota_venta.html', {'venta': venta})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="nota_venta_{venta.codigo_venta}.pdf"'
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    return response




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY", "re_72BPTVXU_GBfnYAHtvn5FtMFShPjb3XVC")

@api_view(['POST'])
def enviar_correo(request):
    try:
        to_email = request.data.get("to","gedalge.cristian22@gmail.com")
        print(to_email)
        subject = request.data.get("subject", "Correo de prueba con Resend")
        message = request.data.get("message", "<p>Hola 👋, esto es una prueba con el SDK oficial.</p>")

        if not to_email:
            return Response({"error": "Debe enviar un campo 'to'."}, status=status.HTTP_400_BAD_REQUEST)

        r = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": to_email,
            "subject": subject,
            "html": message
        })

        return Response({"detail": "Correo enviado correctamente.", "resend_response": r}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

