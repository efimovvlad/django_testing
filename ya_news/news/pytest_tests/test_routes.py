from http import HTTPStatus
import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, urls, expected_status',
    (
        (lazy_fixture('client'), (lazy_fixture('detail')), HTTPStatus.OK),
        (lazy_fixture('client'), (lazy_fixture('home')), HTTPStatus.OK),
        (lazy_fixture('client'), (lazy_fixture('login')), HTTPStatus.OK),
        (lazy_fixture('client'), (lazy_fixture('logout')), HTTPStatus.OK),
        (lazy_fixture('client'), (lazy_fixture('signup')), HTTPStatus.OK),
        (lazy_fixture('not_author_client'), (lazy_fixture('edit')),
         HTTPStatus.NOT_FOUND),
        (lazy_fixture('not_author_client'), (lazy_fixture('delete')),
         HTTPStatus.NOT_FOUND),
        (lazy_fixture('author_client'), (lazy_fixture('edit')),
         HTTPStatus.OK),
        (lazy_fixture('author_client'), (lazy_fixture('delete')),
         HTTPStatus.OK),
    ),
)
def test_pages_availability(
        parametrized_client, urls, expected_status
):
    name, args = urls
    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'urls',
    ((lazy_fixture('edit')), (lazy_fixture('delete'))),
)
def test_redirect(urls, client):
    name, args = urls
    url = reverse(name, args=args)
    login_url = reverse('users:login')
    url_to_login = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, url_to_login)
