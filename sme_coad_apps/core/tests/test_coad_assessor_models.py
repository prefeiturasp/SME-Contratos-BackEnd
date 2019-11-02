import pytest
from model_mommy import mommy

from sme_coad_apps.users.models import User
from ..models import CoadAssessor, Coad

pytestmark = pytest.mark.django_db


@pytest.fixture
def coad():
    return mommy.make(Coad, id=1)


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


def test_append_assessor(fake_user, coad):
    assert CoadAssessor.objects.all().count() == 0
    assessores = [{'assessor': {'username': fake_user.username}}, ]
    CoadAssessor.append_assessores(assessores=assessores)
    assert CoadAssessor.objects.all().count() == 1


def test_limpa_servidor(fake_user, coad):
    mommy.make(CoadAssessor, assessor=fake_user)
    assert CoadAssessor.objects.all().count() == 1
    CoadAssessor.limpa_assessores()
    assert CoadAssessor.objects.all().count() == 0
