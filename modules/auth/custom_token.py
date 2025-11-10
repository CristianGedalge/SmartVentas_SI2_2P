import jwt 
import os
from .models import Usuario

def get_usuario_desde_token_manual(request):
    auth_header = request.headers.get('Authorization')
    # print(auth_header) #solo me imprime el bearer token para testeo
    if not auth_header:
        auth_header = request.META.get('HTTP_AUTHORIZATION')

    if not auth_header or not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]

    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
        user_id = payload.get('user_id')
        return Usuario.objects.get(id=user_id)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Usuario.DoesNotExist):
        return None
