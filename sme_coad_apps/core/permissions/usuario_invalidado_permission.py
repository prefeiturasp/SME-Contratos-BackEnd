from rest_framework.permissions import BasePermission


class UsuarioInvalidadoPermission(BasePermission):

    def has_permission(self, request, view):
        usuario = request.user
        return not usuario.validado
