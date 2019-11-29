from ..serializers.modelo_ateste_serializer import ModeloAtesteSerializer
from ...models.modelo_ateste import ModeloAteste
from ....core.viewsets_abstracts import ComHistoricoViewSet, ComHistoricoReadOnlyViewSet


class ModeloAtesteViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = ModeloAteste.objects.all()
    serializer_class = ModeloAtesteSerializer
