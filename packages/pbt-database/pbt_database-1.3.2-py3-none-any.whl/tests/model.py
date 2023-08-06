from database.shortcuts import sa, sql, i18n, primary_id, Model, Entity


class ModelBook(Model):

    __tablename__ = 'book_i18n'

    id = primary_id()
    title = sa.Column(i18n(), nullable=False)
    author_name = sa.Column(i18n(), nullable=False)
    author_last_name = sa.Column(i18n(), nullable=False)
    pub_year = sa.Column(sql.SmallInteger())


class Book(Entity):

    model = ModelBook
    per_page = 10

    i18n_fields = ('title', 'author_name', 'author_last_name')

    @classmethod
    def queryset(cls, lang) -> sa.sql.Select:
        return sa.select(
            cls.model.id,
            sa.func.coalesce(
                cls.model.title[lang],
                cls.model.title[cls.i18n],
            ).label('title'),
            sa.func.coalesce(
                cls.model.author_name[lang],
                cls.model.author_name[cls.i18n],
            ).label('author_name'),
            sa.func.coalesce(
                cls.model.author_last_name[lang],
                cls.model.author_last_name[cls.i18n],
            ).label('author_last_name'),
            cls.model.pub_year,
        ).order_by(cls.model.id.asc())
