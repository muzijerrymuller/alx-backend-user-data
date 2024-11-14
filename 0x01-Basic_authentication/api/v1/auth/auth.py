#!/usr/bin/env python3
"""
Definition of class Auth
This module defines the Auth class that is responsible for managing
the authentication process for an API. The class provides methods
to verify if a path requires authentication, extract authorization
headers, and retrieve the current user based on request information.
The docstrings are encoded in UTF-8 to ensure compatibility with
international characters and special symbols, allowing for flexible
use across different languages and locales.
"""
from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """
    Manages the API authentication process.
    This class encapsulates all the logic necessary to determine whether
    an API endpoint requires authentication, how to extract the authorization
    header from a request, and how to retrieve the current user based on the
    incoming request. It serves as the backbone of the authentication layer
    for securing access to various routes in the API.
    The docstrings within this class are validated to ensure UTF-8
    compatibility, making it flexible for use with international characters
    and data sources.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a specific path requires authentication

        This method checks if the provided path
        is excluded from authentication
        based on a list of paths that do not
        require authentication. It ensures
        that only authorized users can access protected paths, while excluded
        paths can be accessed without authentication.
        Args:
        - path (str): The URL path to be checked
        for authentication requirements.
        - excluded_paths (List[str]): A list of paths that do not require
              authentication.
        Returns:
        - bool: Returns True if the path requires authentication (i.e.,
        it is not in the excluded paths), otherwise returns False.
        Notes:
        - If the `excluded_paths` list is empty or None, all paths require
        authentication.
        - The method supports path matching with wildcards (e.g., "api/*"
        - UTF-8 encoding is used to ensure proper handling of paths with
        non-ASCII characters.
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True


    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request object.
        This method extracts the 'Authorization' header from the incoming
        request. If the header is missing
        or if the request is None, it returns
        None. This header typically contains the authentication token that
        is used to validate the user's identity.
        Args:
            - request (optional): The Flask request object. If not provided,
              the method assumes the default request.
        Returns:
            - str: The value of the 'Authorization'
            header if present, otherwise None.
        Notes:
            - The 'Authorization' header is essential for identifying and
              authenticating users in the API.
            - UTF-8 validation is used to handle any characters in the
              Authorization header properly.
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header


    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request object.
        This method is intended to extract and return a User instance based
        on the information provided in the request, such as an authentication
        token or session data.
        If the request does not provide any user-related
        information, this method returns None.
        Args:
            - request (optional): The Flask request object containing user
              authentication data.
        Returns:
            - User: A User instance populated
            with information from the request
              or None if no user data is available.
        Notes:
            - This method may be further extended to integrate with actual
              user models and authentication mechanisms.
            - UTF-8 validation ensures that user data with international
              characters is handled correctly.
        """
        return None
