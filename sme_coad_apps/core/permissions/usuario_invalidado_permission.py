from rest_framework.permissions import BasePermission


class UsuarioInvalidadoPermission(BasePermission):

    def has_permission(self, request, view):
        usuario = request.user
        if usuario == 'AnonymousUser':
            return False
        else:
            return usuario.validado
