import pytest

pytestmark = pytest.mark.django_db

# def test_contrato_unidade_viewset(faker_user):
#     request = APIRequestFactory().get("")
#     contrato_unidade_detalhe = ContratoUnidadeViewSet.as_view({'get': 'retrieve'})
#     force_authenticate(request, user=faker_user)
#     contrato = mommy.make('Contrato')
#
#     response = contrato_unidade_detalhe(request, uuid=contrato.uuid)
#
#     assert response.status_code == status.HTTP_200_OK
