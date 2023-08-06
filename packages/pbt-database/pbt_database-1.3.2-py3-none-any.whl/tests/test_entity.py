from .model import Book


various_books = [
    {
        'title': 'Вязальные приключения с гиперболическими плоскостями',
        'pub_year': 2009,
        'author_name': 'Дайна',
        'author_last_name': 'Тайминя',
    },
    {
        'title': 'Жареные зеленые помидоры',
        'pub_year': 1798,
        'author_name': 'Фенни',
        'author_last_name': 'Флег',
    },
    {
        'title': 'Москва-ква-ква',
        'pub_year': 2008,
        'author_name': 'Остров',
        'author_last_name': 'Аксенов',
    },
    {
        'title': 'Негожи лилиям прясть',
        'pub_year': 2010,
        'author_name': 'Морис',
        'author_last_name': 'Дрюон',
    },
    {
        'title': 'Зверочеловекоморок',
        'pub_year': 2003,
        'author_name': 'Тадеуш',
        'author_last_name': 'Конвицкий',
    },
    {
        'title': 'Маленькая хня',
        'pub_year': 2006,
        'author_name': 'Лора',
        'author_last_name': 'Белоиван',
    },
    {
        'title': 'Хочу бабу на роликах',
        'pub_year': 2003,
        'author_name': 'Вильмонт',
        'author_last_name': 'Екатерина',
    },
    {
        'title': 'Водоросль',
        'pub_year': 1950,
        'author_name': 'Денис',
        'author_last_name': 'Фонвизин',
    },
    {
        'title': 'Пахом звонит в колокол',
        'pub_year': 1920,
        'author_name': 'Хомен',
        'author_last_name': 'Нгуэй',
    },
    {
        'title': 'Старуха Баскервиль',
        'pub_year': 1910,
        'author_name': 'Максим',
        'author_last_name': 'Горький',
    },
    {
        'title': 'Протез',
        'pub_year': 1952,
        'author_name': 'Франц',
        'author_last_name': 'Кафка',
    },
    {
        'title': 'Приключения Екль Бирифина',
        'pub_year': 1920,
        'author_name': 'Марк',
        'author_last_name': 'Твер',
    },
]


async def test_i18n(session):
    """Test i18n support."""
    lang = 'en'

    for num, sample in enumerate(various_books, start=1):
        created = await Book.add(fields=sample)
        assert created['id'] == num
        assert created['title'] == sample['title']

        readed = await Book.read(id=num, lang=Book.i18n)
        assert readed['id'] == created['id']
        assert readed['title'] == created['title']

        new_title = f"{readed['title']} - second edition"
        edited = await Book.edit(
            id=num,
            fields={'title': new_title},
            lang=Book.i18n,
        )
        assert edited['id'] == readed['id'] == num
        assert new_title == edited['title']

        translate = {
            'title': sample['title'] + f'_{lang}',
            'author_name': sample['author_name'] + f'_{lang}',
            'author_last_name': sample['author_last_name'] + f'_{lang}',
        }

        _i18n = await Book.translate(num, fields=translate, lang=lang)

        assert str(_i18n['title']).endswith(lang)
        assert str(_i18n['author_name']).endswith(lang)
        assert str(_i18n['author_last_name']).endswith(lang)

        _i18n_book = await Book.read(num, lang=lang)
        assert _i18n_book == _i18n

    first_page = await Book.read_page(lang=Book.i18n, page=1)
    assert first_page['page'] == 1
    assert first_page['count'] == len(various_books)
    assert first_page['limit'] == Book.per_page
    assert first_page['last_page'] == 2
    assert len(first_page['results']) == Book.per_page

    for num, sample in enumerate(various_books, start=1):
        if num >= Book.per_page:
            break

        update_title = f"{various_books[num]['title']} - second edition"
        assert first_page['results'][num]['title'] == update_title

    second_page = await Book.read_page(Book.i18n, page=2)

    assert second_page['page'] == 2
    assert second_page['count'] == len(various_books)
    assert second_page['limit'] == Book.per_page
    assert second_page['last_page'] == 2
    assert len(second_page['results']) == len(various_books) - Book.per_page
    assert second_page['results'][0]['id'] == Book.per_page + 1

    for num, sample in enumerate(various_books[10:], start=0):
        update_title = f"{sample['title']} - second edition"
        assert second_page['results'][num]['title'] == update_title
        assert second_page['results'][num]['id'] == Book.per_page + num + 1

        # Check delete
        await Book.delete(id=second_page['results'][num]['id'])

    page = await Book.read_page(lang=Book.i18n, page=1)
    assert page['page'] == 1
    assert page['count'] == len(various_books) - 2
    assert page['limit'] == Book.per_page
    assert page['last_page'] == 1
    assert len(page['results']) == len(various_books) - 2

    page = await Book.read_page(lang=lang, page=1)
    for obj in page['results']:
        assert str(obj['title']).endswith(lang)
