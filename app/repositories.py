from typing import Optional, Any

from sqlalchemy import or_

from app.models import User


class UserRepository:
    def get_paginated(
        self, page: int, per_page: int, search_query: Optional[str] = None
    ) -> Any:
        """
        Возвращает пагинированный список пользователей с поиском.
        """
        query = User.query
        if search_query:
            search_pattern = f"%{search_query}%"
            query = query.filter(
                or_(
                    User.username.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                )
            )
        return query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Поиск пользователя по ID.
        """
        return User.query.get(user_id)

    def find_by_username(self, username: str) -> Optional[User]:
        """
        Поиск пользователя по имени.
        """
        return User.query.filter_by(username=username).first()

    def find_by_email(self, email: str) -> Optional[User]:
        """
        Поиск пользователя по почте.
        """
        return User.query.filter_by(email=email).first()

    def create(self, username: str, email: str, db_session) -> User:
        """
        Создает нового пользователя.
        """
        user = User(username=username, email=email)
        db_session.add(user)
        db_session.commit()
        return user

    def update(self, user: User, username: str, email: str, db_session) -> User:
        """
        Обновляет данные пользователя.
        """
        user.username = username
        user.email = email
        db_session.commit()
        return user

    def delete(self, user: User, db_session) -> None:
        """
        Удаляет пользователя из БД.
        """
        db_session.delete(user)
        db_session.commit()
