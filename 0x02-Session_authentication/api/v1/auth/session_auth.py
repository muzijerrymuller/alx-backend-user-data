#!/usr/bin/env python3
"""
Definition of the SessionAuth class for session-based authentication.
"""

import base64
from uuid import uuid4
from typing import TypeVar

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Session-based authentication class.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a user based on the provided user ID.
        Args:
            user_id (str): The ID of the user for whom
            the session is being created.
        Returns:
            str: The session ID if the user ID is valid.
            None: If the user ID is None or not a string.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = uuid4()
        self.user_id_by_session_id[str(session_id)] = user_id
        return str(session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a given session ID.
        Args:
            session_id (str): The session ID whose user ID is being retrieved.
        Returns:
            str: The user ID corresponding to the session ID.
            None: If the session ID is invalid or not provided.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the user instance associated with the
        current session, based on the session cookie.
        Args:
            request: The request object containing the session cookie.
        Returns:
            User: The user instance associated with the session.
            None: If no user is found for the session.
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Destroys the current session by deleting the associated session ID.
        Args:
            request: The request object containing the session cookie.
        Returns:
            bool: True if the session was successfully
            destroyed, False otherwise.
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
