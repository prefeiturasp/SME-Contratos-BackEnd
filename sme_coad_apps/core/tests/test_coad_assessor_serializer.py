import pytest
from model_mommy import mommy

from sme_coad_apps.users.models import User
from ..api.serializers.coad_assessor_serializer import CoadAssessorSerializer
from ..models import CoadAssessor

pytestmark = pytest.mark.django_db


def test_coad_assessor_serializer():
    assessor = mommy.make(User)
    model = mommy.make(CoadAssessor, assessor=assessor)

    serializer = CoadAssessorSerializer(model)

    assert serializer.data is not None
    assert serializer.data['assessor']
    assert serializer.data['coad']
    assert serializer.data['id']
