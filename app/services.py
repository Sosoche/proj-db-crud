import logging
from typing import Optional, Tuple, Any

from app.repositories import UserRepository
from app.models import db, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_users_list(
        self, page: int, per_page: int, search: Optional[str] = None
    ) -> Any:
        """
        Возвращает список пользователей.
        """
        return self.repository.get_paginated(page, per_page, search)

    def create_user(self, username: str, email: str) -> Tuple[bool, str]:
        """
        Создает пользователя с проверкой уникальности.
        """
        if self.repository.find_by_username(username):
            logger.warning(f"Create failed: {username} exists.")
            return False, "Username already exists."
        if self.repository.find_by_email(email):
            logger.warning(f"Create failed: {email} exists.")
            return False, "Email already exists."

        self.repository.create(username, email, db.session)
        logger.info(f"User created: {username}")
        return True, "User created successfully."

    def update_user(
        self, user_id: int, username: str, email: str
    ) -> Tuple[bool, str]:
        """
        Обновляет пользователя.
        """
        user = self.repository.find_by_id(user_id)
        if not user:
            logger.error(f"Update failed: ID {user_id} not found.")
            return False, "User not found."

        existing_user = self.repository.find_by_username(username)
        if existing_user and existing_user.id != user_id:
            return False, "Username already taken."

        existing_email = self.repository.find_by_email(email)
        if existing_email and existing_email.id != user_id:
            return False, "Email already taken."

        self.repository.update(user, username, email, db.session)
        logger.info(f"User updated: ID {user_id}")
        return True, "User updated successfully."

    def delete_user(self, user_id: int) -> Tuple[bool, str]:
        """
        Удаляет пользователя.
        """
        user = self.repository.find_by_id(user_id)
        if not user:
            logger.error(f"Delete failed: ID {user_id} not found.")
            return False, "User not found."

        self.repository.delete(user, db.session)
        logger.info(f"User deleted: ID {user_id}")
        return True, "User deleted successfully."

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Возвращает пользователя по ID.
        """
        return self.repository.find_by_id(user_id)
