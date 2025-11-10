from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os 
import google.generativeai as genai
from django.db import connection
import re
@api_view(['GET'])
def prueba(request):
    print(os.getenv("GEMINI_API_KEY"))
    prompt = request.data.get("prompt")

    if not prompt:
        return Response({"error": "Debes enviar un campo 'prompt'."},
            status=status.HTTP_400_BAD_REQUEST)

    # Esquema de la base (define tus tablas principales)
    schema_description = """
        Tablas disponibles y sus columnas principales:

1️. producto
- id (PK)
- categoria_id (FK → categoria.id)
- marca_id (FK → marca.id)
- nombre (nombre único del producto)
- descripcion (texto)
- url_img (URL de imagen)
- precio (decimal)
- stock (entero)
- estado (booleano, True = activo)
- tiempo_garantia (entero, meses)
- tipo_garantia (texto: 'FABRICANTE', 'TIENDA' o 'NINGUNO')
- fecha (fecha de creación del producto)
        """
    model = genai.GenerativeModel(
        model_name="gemini-2.5-pro"
    )

    query_prompt = f"""
        Eres un generador de consultas SQL seguras para PostgreSQL.
        Dado este esquema:
        {schema_description}

        Escribe una consulta SQL de solo lectura (SELECT) para responder:
        "{prompt}"

        IMPORTANTE:
        - No uses DELETE, DROP, UPDATE ni INSERT.
        - Usa nombres de columnas y tablas tal como aparecen en el esquema.
        - Devuelve solo la consulta SQL, sin explicaciones.
        """

    try:
        gemini_response = model.generate_content(query_prompt)
        sql_query = gemini_response.text
        query_clean = re.sub(r"```sql|```", "", sql_query).strip()

        # Validación básica
        if re.search(r"\b(drop|delete|update|insert)\b", sql_query, re.IGNORECASE):
            return Response({"error": "Consulta potencialmente peligrosa bloqueada."},
            status=status.HTTP_400_BAD_REQUEST)

        # Ejecutar la consulta en PostgreSQL
        with connection.cursor() as cursor:
            cursor.execute(query_clean)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]

        return Response({
            "query": query_clean,
            "resultados": data
        })

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
