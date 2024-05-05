from http import HTTPStatus
import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture
from news.models import Comment


@pytest.mark.django_db
def test_pages_availability(client, urls):
    for name, args in urls:
        url = reverse(name, args=args)
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
# Не совсем понял как объединить эти два теста.
# В первом проверяется доступность страниц для анонимного пользователя.
# Во втором авторизованные пользователи где для каждого запроса
# будут получены конкретные статусы. Если объединю и также пойду в цикле то
# нужно для каждого пользователя конкретно указать какие статусы
# будут получены по каждому запросу. В теории на unittest пошли
# таким же путем как написан сейчас.


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_availability_for_comment_edit_and_delete(
        parametrized_client, name, comment, expected_status
):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', lazy_fixture('comment_id')),
        ('news:delete', lazy_fixture('comment_id')),
    ),
)
def test_redirect_for_anonymous_client(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


def test_redirect_user_create_edit_delete_comment(
        author_client, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    url_to_comments = url + '#comments'
    response = author_client.post(url, data={'text': 'Текст'})
    assertRedirects(response, url_to_comments)
    comment = Comment.objects.get()
    edit_url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, url_to_comments)
    delete_url = reverse('news:delete', args=(comment.id,))
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
