from ..serializers.coad_assessor_serializer import CoadAssessorSerializer

from ...models import CoadAssessor
from ...viewsets_abstracts import ComHistoricoViewSet


class CoadAssessorViewSet(ComHistoricoViewSet):
    queryset = CoadAssessor.objects.all()
    serializer_class = CoadAssessorSerializer
