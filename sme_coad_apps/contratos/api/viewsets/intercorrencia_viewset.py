from rest_framework.decorators import action
from rest_framework.response import Response

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...api.serializers.intercorrencia_serializer import IntercorrenciaCreateSerializer, IntercorrenciaSerializer
from ...models.intercorrencia import Intercorrencia


class IntercorrenciaViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Intercorrencia.objects.all()
    serializer_class = IntercorrenciaSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return IntercorrenciaSerializer
        else:
            return IntercorrenciaCreateSerializer

    @action(detail=False, url_path='motivos-suspensao', methods=['get'])
    def lista_motivos_suspensao_intercorrencias(self, _):
        return Response(Intercorrencia.motivos_suspensao_to_json())
