import pytest

from django.urls import reverse

URL = reverse('news:home')
DETAIL_URL = 'news:detail'


@pytest.mark.django_db
def test_news_count(client, all_news):
    response = client.get(URL)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == all_news - 1


@pytest.mark.django_db
def test_news_order(client, all_news):
    response = client.get(URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, news, comments_order):
    url = reverse(DETAIL_URL, args=(news.id,))
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news):
    url = reverse(DETAIL_URL, args=(news.id,))
    response = client.get(url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, news):
    url = reverse(DETAIL_URL, args=(news.id,))
    response = author_client.get(url)
    assert 'form' in response.context
