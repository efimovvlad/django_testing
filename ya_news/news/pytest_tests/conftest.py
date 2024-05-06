import pytest
from datetime import datetime, timedelta
from django.test.client import Client
from news.models import News, Comment
from yanews import settings


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(title='Заголовок', text='Текст')
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст'
    }


@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def comments(news, author):
    for index in range(10):
        Comment.objects.create(
            news=news,
            author=author,
            text=f'Tекст {index}',
        )
    return news


@pytest.fixture
def home():
    return 'news:home', None


@pytest.fixture
def detail(news):
    return 'news:detail', (news.id,)


@pytest.fixture
def edit(comment):
    return 'news:edit', (comment.id,)


@pytest.fixture
def delete(comment):
    return 'news:delete', (comment.id,)


@pytest.fixture
def login():
    return 'users:login', None


@pytest.fixture
def logout():
    return 'users:logout', None


@pytest.fixture
def signup():
    return 'users:signup', None
