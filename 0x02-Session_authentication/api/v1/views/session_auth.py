#!/usr/bin/env python3
"""
Module defining the SessionAuth class, responsible for implementing
session-based authentication methods for the application.
"""

import base64
from uuid import uuid4
from typing import TypeVar
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Implements the session-based authorization protocol for managing
    user authentication and session handling.
    Attributes:
        user_id_by_session_id (dict): A dictionary mapping session IDs
        to corresponding user IDs, allowing for session-to-user association.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Generates a unique session ID and associates it with the provided user ID.
        Args:
            user_id (str): The unique identifier of a user.
        Returns:
            str: A unique session ID if user_id is valid.
            None: If the provided user_id is invalid (None or not a string).
        This method uses the `uuid4` function to generate a unique identifier
        for the session. The mapping of session ID to user ID is stored in
        the `user_id_by_session_id` dictionary for later retrieval.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves a user ID associated with a given session ID.
        Args:
        session_id (str): The session ID whose associated user ID is sought
        Returns:
         str: The user ID associated with the session ID.
        None: If session_id is invalid (None or not a string).
        This method checks the `user_id_by_session_id` dictionary for the
        given session ID and returns the corresponding user ID if it exists.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the current user based on the session cookie from request.
        Args:
            request: The HTTP request object containing session cookie data.
        Returns:
            User: The user instance associated with the session cookie.
            None: If no user is associated with the session or the session
            cookie is invalid.
        This method combines session cookie retrieval, session ID-to-user ID
        mapping, and user instance fetching for identifying the current user.
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id:
            return User.get(user_id)
        return None

    def destroy_session(self, request=None) -> bool:
        """
        Terminates an active user session by deleting the session ID mapping.
        Args:
            request: The HTTP request object containing the session cookie.
        Returns:
        bool: True if the session was successfully destroyed.
        False: If the request object is invalid
        or the session ID does not exist.
        This method deletes the session ID from the `user_id_by_session_id`
        dictionary, effectively logging the user out.
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        if session_cookie in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_cookie]
            return True
        return False
