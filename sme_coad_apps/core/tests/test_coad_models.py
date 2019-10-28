import pytest
from django.contrib import admin
from model_mommy import mommy

from sme_coad_apps.users.models import User
from ..models_abstracts import SingletonModel

from ..admin import CoadAdmin
from ..models import Coad, CoadAssessor

pytestmark = pytest.mark.django_db


def test_instance_model():
    coordenador = mommy.make(User)
    model = Coad.objects.create(coordenador=coordenador)
    assert isinstance(model, SingletonModel)
    assert isinstance(model, Coad)
    assert isinstance(model.coordenador, User)
    assert model.historico
    assert model.assessores


def test_srt_model():
    model = Coad.objects.create()
    assert model.__str__() == "COAD (Registro Único)"


def test_meta_modelo():
    model = Coad.objects.create()
    assert model._meta.verbose_name == 'COAD'
    assert model._meta.verbose_name_plural == 'COAD'


def test_admin():
    model_admin = CoadAdmin(Coad, admin.site)
    # pylint: disable=W0212
    assert admin.site._registry[Coad]


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
