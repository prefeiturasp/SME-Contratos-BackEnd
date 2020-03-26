from ..serializers.coad_assessor_serializer import CoadAssessorSerializer, CoadAssessorCreateSerializer

from ...models import CoadAssessor
from ...viewsets_abstracts import ComHistoricoViewSet


class CoadAssessorViewSet(ComHistoricoViewSet):
    queryset = CoadAssessor.objects.all()
    serializer_class = CoadAssessorSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CoadAssessorSerializer
        elif self.action == 'list':
            return CoadAssessorSerializer
        else:
            return CoadAssessorCreateSerializer
