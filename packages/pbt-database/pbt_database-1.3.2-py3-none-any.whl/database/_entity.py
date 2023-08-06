import math

from typing import Dict, Sequence, Optional
from sqlalchemy import select, update, delete, func, Column

from sqlalchemy.sql import Select

from ._model import Model
from ._connection import make_session


class Entity:

    model: Model

    per_page: int = 20

    i18n: str = 'ru'
    i18n_fields: Sequence[str] = None

    @classmethod
    def _get_fields(cls) -> Dict[str, Column]:
        """Raw model."""
        return {c.name: c for c in cls.model.__table__.columns}

    @staticmethod
    def _dict(row) -> Dict:
        """Row to dict."""
        row = row.__dict__
        row.pop('_sa_instance_state', None)
        return row

    @classmethod
    def queryset(cls, lang: str) -> Select:
        """Object queryset."""
        raise NotImplemented()

    @classmethod
    async def add(cls, fields: Dict) -> Dict:
        """Add """
        model_fields = cls._get_fields()

        obj_dict = {}
        for new_field, new_value in fields.items():
            if new_field not in model_fields:
                continue
            if new_field in cls.i18n_fields:
                obj_dict[new_field] = {cls.i18n: new_value}
            else:
                obj_dict[new_field] = new_value

        obj = cls.model(**obj_dict)  # noqa

        async with make_session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            fields.update({'id': obj.id})
            return fields

    @classmethod
    async def read(cls, id: int, lang: str) -> Optional[Dict]:
        """Read one."""
        query = cls.queryset(lang=str(lang).lower()).where(cls.model.id == id)
        async with make_session() as session:
            result = await session.execute(query)
            row = result.fetchone()
            return row._asdict() if row else None

    @classmethod
    async def edit(cls, id: int, fields: Dict, lang: str) -> Optional[Dict]:
        """Update one."""
        async with make_session() as session:
            # Fetch origin
            origin = await session.get(cls.model, id)
            if not origin:
                # Not found
                return

            origin = cls._dict(origin)
            # Update origin with i18n
            for edit_field, edit_value in fields.items():
                if edit_field not in origin:
                    continue
                elif not cls.i18n_fields or edit_field not in cls.i18n_fields:
                    origin[edit_field] = edit_value
                else:
                    origin[edit_field].update({cls.i18n: edit_value})
            # Update instance
            origin.pop('id', None)
            update_query = update(cls.model).filter_by(id=id).values(**origin)
            await session.execute(update_query)
            await session.commit()
            # Retrieve update
            return await cls.read(id, lang=str(lang).lower())

    @classmethod
    async def read_page(cls, lang: str, page: int = 1) -> Dict:
        """Read all."""
        count = await cls.count()
        last_page = int(math.ceil(count / float(cls.per_page)))

        offset = 0 if page <= 1 else (page - 1) * cls.per_page

        query = cls.queryset(lang=str(lang).lower())
        query = query.offset(offset).limit(cls.per_page)

        async with make_session() as session:
            rows = await session.execute(query)
            rows = [row._asdict() for row in rows.all()]
            return {
                'limit': cls.per_page,
                'last_page': last_page if last_page else 1,
                'count': count,
                'page': page,
                'results': rows,
            }

    @classmethod
    async def count(cls) -> int:
        """Read all."""
        async with make_session() as session:
            query = select(
                [func.count('*')]
            ).select_from(
                cls.queryset(lang=cls.i18n).order_by(None)
            )
            total = await session.execute(query)
            return total.scalar()

    @classmethod
    async def delete(cls, id: int) -> None:
        """Delete object."""
        async with make_session() as session:
            await session.execute(delete(cls.model).filter_by(id=id))
            await session.commit()

    @classmethod
    async def translate(
        cls,
        id: int,
        lang: str,
        fields: Dict,
    ) -> Optional[Dict]:
        """Delete object."""
        async with make_session() as session:
            # Fetch origin
            origin = await session.get(cls.model, id)
            if not origin:
                # Not found
                return

            origin = cls._dict(origin)
            # Update origin with i18n
            for edit_field, edit_value in fields.items():
                if edit_field not in origin:
                    continue
                elif not cls.i18n_fields or edit_field not in cls.i18n_fields:
                    origin[edit_field] = edit_value
                else:
                    origin[edit_field].update({str(lang).lower(): edit_value})
            # Update instance
            origin.pop('id', None)
            update_query = update(cls.model).filter_by(id=id).values(**origin)
            await session.execute(update_query)
            await session.commit()
            # Retrieve update
            return await cls.read(id, lang=str(lang).lower())
