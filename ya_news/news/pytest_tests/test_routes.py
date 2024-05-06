from http import HTTPStatus
import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lazy_fixture('client'), HTTPStatus.FOUND),
        (lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'urls',
    (
        (lazy_fixture('edit')),
        (lazy_fixture('delete')),
        (lazy_fixture('home')),
        (lazy_fixture('detail')),
        (lazy_fixture('login')),
        (lazy_fixture('logout')),
        (lazy_fixture('signup')),
    ),
)
def test_pages_availability(
        parametrized_client, urls, expected_status
):
    name, args = urls
    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    if name == 'news:edit' or name == 'news:delete':
        assert response.status_code == expected_status
    else:
        assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client',
    (
        (lazy_fixture('client')),
        (lazy_fixture('author_client'))
    ),
)
@pytest.mark.parametrize(
    'urls',
    (
        (lazy_fixture('detail')),
        (lazy_fixture('edit')),
        (lazy_fixture('delete')),
    ),
)
def test_redirect(
        parametrized_client, urls, client, author_client, form_data, news):
    name, args = urls
    url = reverse(name, args=args)
    login_url = reverse('users:login')
    detail_url = reverse('news:detail', args=(news.id,))
    url_to_login = f'{login_url}?next={url}'
    url_to_comments = detail_url + '#comments'
    if parametrized_client == client and name != 'news:detail':
        response = parametrized_client.get(url)
        assertRedirects(response, url_to_login)
    if parametrized_client == author_client and name != 'news:delete':
        response = parametrized_client.post(url, data=form_data)
        assertRedirects(response, url_to_comments)
    if parametrized_client == author_client and name == 'news:delete':
        response = parametrized_client.delete(url)
        assertRedirects(response, url_to_comments)
