from rest_framework import permissions


class UsuarioValidadoPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        usuario = request.user
        return usuario.validado
