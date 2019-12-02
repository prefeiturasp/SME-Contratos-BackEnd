from ..serializers.modelo_ateste_serializer import ModeloAtesteSerializer, ModeloAtesteLookUpSerializer
from ...models.modelo_ateste import ModeloAteste
from ....core.viewsets_abstracts import ComHistoricoViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


class ModeloAtesteViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = ModeloAteste.objects.all()
    serializer_class = ModeloAtesteSerializer

    @action(detail=False, url_path='titulos-modelo-ateste')
    def lookup(self, _):
        return Response(ModeloAtesteLookUpSerializer(self.queryset.order_by('-criado_em'), many=True).data)
