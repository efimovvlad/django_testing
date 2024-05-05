import pytest
from datetime import datetime, timedelta
from django.utils import timezone
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


# Если убрать две нижние фикстуры то нужно будет
# придумывать другое решение при использовании lazy_fixture.
# Попробовал обойтись без этих фикстур и вроде бы получается
# только больше строк кода. В местах где идет цикл урлов,
# в аргументы подставляется либо None либо передаваемый аргумент.
# Если попробовать применить к аргументу .id то возникает ошибка.
# Полагаю можно добавить дополнительный if но в таком случае
# строк кода станет больше. В теории предлагалось именное
# такое решение как написано сейчас.
# Либо может есть вариант решения который я ещё не понял.
@pytest.fixture
def news_id(news):
    return (news.id,)


@pytest.fixture
def comment_id(comment):
    return (comment.id,)


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
    now = timezone.now()
    for index in range(10):
        Comment.objects.create(
            news=news,
            author=author,
            text=f'Tекст {index}',
            created=now + timedelta(days=index)
        )
        # comment.created = now + timedelta(days=index)
        # comment.save()
        # Могу сразу прописать поле created, но в теории рекомендовали
        # менять значение после создания комментария:
        # "Даже если передать в комментарии разные значения поля created,
        # то в базу всё равно запишутся значения текущего времени. И с
        # высокой вероятностью для двух объектов, создаваемых подряд,
        # это время будет одинаковым: программный код работает быстро."
    return news


@pytest.fixture
def urls(news_id):
    return (
        ('news:detail', news_id),
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    )
