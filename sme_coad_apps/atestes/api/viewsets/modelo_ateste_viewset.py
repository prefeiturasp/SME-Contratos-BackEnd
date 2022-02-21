from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers.modelo_ateste_serializer import (ModeloAtesteSerializer, ModeloAtesteLookUpSerializer,
                                                    ModeloAtesteSerializerCreate)
from ...models.modelo_ateste import ModeloAteste
from ....core.viewsets_abstracts import ComHistoricoViewSet


class ModeloAtesteViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = ModeloAteste.objects.all()
    serializer_class = ModeloAtesteSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ModeloAtesteSerializer
        elif self.action == 'list':
            return ModeloAtesteLookUpSerializer
        else:
            return ModeloAtesteSerializerCreate

    @action(detail=False, url_path='titulos-modelo-ateste')
    def lookup(self, _):
        return Response(ModeloAtesteLookUpSerializer(self.queryset.order_by('-criado_em'), many=True).data)
