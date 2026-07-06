from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings

from .models import Bibliotecario, Usuario

TIPO_ACTOR_CLAIM = 'tipo_actor'
TIPO_ACTOR_USUARIO = 'USUARIO'
TIPO_ACTOR_BIBLIOTECARIO = 'BIBLIOTECARIO'


class ActorJWTAuthentication(JWTAuthentication):
    """Resuelve request.user contra Usuario o Bibliotecario segun el claim tipo_actor del token."""

    def get_user(self, validated_token):
        try:
            actor_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken('El token no contiene un identificador de actor.')

        tipo_actor = validated_token.get(TIPO_ACTOR_CLAIM, TIPO_ACTOR_USUARIO)
        modelo = Bibliotecario if tipo_actor == TIPO_ACTOR_BIBLIOTECARIO else Usuario

        try:
            actor = modelo.objects.get(**{api_settings.USER_ID_FIELD: actor_id})
        except modelo.DoesNotExist:
            raise AuthenticationFailed('El actor asociado al token ya no existe.', code='user_not_found')

        if not actor.is_active:
            raise AuthenticationFailed('La cuenta del actor esta inactiva.', code='user_inactive')

        return actor
