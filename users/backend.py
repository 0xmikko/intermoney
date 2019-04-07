from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import HTTP_HEADER_ENCODING, exceptions


class EthereumAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """
        Returns a `User` if a correct username and password have been supplied
        using HTTP Basic authentication.  Otherwise returns `None`.
        """
        auth = get_authorization_header(request).split()

        username = ""

        for a in auth:
            if a.startswith(b"Auth="):
                username = a.replace(b"Auth=", b"")

        if username == "":
            msg = "No user address was found"
            return (None, None)

        print(username)

        USER_MODEL = get_user_model()

        users = USER_MODEL.objects.filter(username=username)
        print(users.count())
        if users.count() == 0:
            user = USER_MODEL.objects.create_user(username=username, password=hash(username))
        else:
            user = users[0]

        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (user, None)

