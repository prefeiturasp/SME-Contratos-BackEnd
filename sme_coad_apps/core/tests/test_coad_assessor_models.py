import pytest
from model_mommy import mommy

from sme_coad_apps.users.models import User
from ..models import CoadAssessor

pytestmark = pytest.mark.django_db


def test_instance_assessor_model():
    assessor = mommy.make(User)
    model = mommy.make(CoadAssessor, assessor=assessor)
    assert isinstance(model, CoadAssessor)
    assert isinstance(model.assessor, User)
    assert model.historico


def test_srt_assessor_model():
    assessor = mommy.make(User, nome='Teste')
    model = mommy.make(CoadAssessor, assessor=assessor)
    assert model.__str__() == "Teste"


def test_meta_assessor_modelo():
    assessor = mommy.make(User, nome='Teste')
    model = mommy.make(CoadAssessor, assessor=assessor)
    assert model._meta.verbose_name == 'Assessor COAD'
    assert model._meta.verbose_name_plural == 'Assessores COAD'
