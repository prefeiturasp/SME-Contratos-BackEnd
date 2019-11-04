from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers.nucleo_serializer import NucleoSerializer, NucleoLookUpSerializer, NucleoCreateSerializer
from ..serializers.servidor_serializer import ServidorSerializer
from ...models import Nucleo
from ...services import limpa_servidores_nucleo, update_servidores_nucleo
from ...viewsets_abstracts import ComHistoricoViewSet


class NucleoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Nucleo.objects.select_related('divisao').all()
    serializer_class = NucleoSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NucleoSerializer
        elif self.action == 'list':
            return NucleoSerializer
        else:
            return NucleoCreateSerializer

    @action(detail=False)
    def lookup(self, _):
        return Response(NucleoLookUpSerializer(self.queryset, many=True).data)

    @action(detail=True, url_path='limpa-servidores', methods=['delete'])
    def limpa_servidores(self, _, uuid=None):
        nucleo = self.get_object()
        limpa_servidores_nucleo(nucleo=nucleo)

        return Response({'message': f'Todos os servidores do Nucleo {nucleo.sigla} foram apagados'})

    @action(detail=True, url_path='update-servidores', methods=['post'])
    def update_servidores(self, request, uuid=None):
        nucleo = self.get_object()
        servidores = request.data['servidores']
        update_servidores_nucleo(servidores=servidores, nucleo=nucleo)
        return Response([{'message': f'Servidores adicionados ao núcleo {nucleo.sigla}'}, {'servidores': servidores}])

    @action(detail=True, url_path='servidores', methods=['get'])
    def servidores(self, _, uuid=None):
        nucleo = self.get_object()
        servidores = nucleo.servidores.all()
        serializer = ServidorSerializer(servidores, many=True)
        return Response(serializer.data)
