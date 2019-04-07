import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponseBadRequest
from django.utils.html import strip_tags


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Account class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email=None, password=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if User.objects.filter(email=username).count() >0:
            print("FUC")
            raise ValueError('User with this username is already exists')

        user = self.model(username=username, email=username)
        user.set_password(password)
        user.save()

        # All users should be verified using email confirmation
        user.send_verification_mail()

        # Send notification for new user registration
        send_system_notification("TS Notification: New user registered", "New user %s was registered" % email)

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(db_index=True, max_length=255, unique=True)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True)


    # When a user no longer wishes to use our platform, they may try to delete
    # their account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. We
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users this flag will always be
    # false.
    is_staff = models.BooleanField(default=False)

    # Flag that email is verified
    is_verified = models.BooleanField(default=False)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    def authenficate_email(self) -> None:
        from events.models import Event
        self.is_verified = True
        self.save()
        Event.add_event(user=self, event=Event.EMAIL_VERIFIED)

    def send_verification_mail(self) -> None:
        """
        Send verification email for new users
        :return:
        """
        from events.models import Event
        new_token = EmailToken.generate_token(self)
        print(new_token)
        html_message = render_to_string('email/verification_email.html',
                                        {'action_url': ('https://alpha.tokenstarter.io/verify-email/' + new_token) })

        self.send_email("Welcome to Tokenstarter", html_message=html_message)
        Event.add_event(self, Event.VERIFICATION_EMAIL_SENT)

    def send_email(self, subject: str, html_message: str):
        """
        Sends Email to user
        :return:
        """
        plain_message = strip_tags(html_message)

        msg = EmailMultiAlternatives(from_email='noreply@tokenstarter.io',
                                     to=[self.email],
                                     subject=subject,
                                     body=plain_message)
        msg.attach_alternative(html_message, "text/html")

        msg.send()


def send_system_notification(subject: str, message: str):
    """
    Send system notificaiton to superuser via email
    :param message:
    :return:
    """
    user = User.objects.filter(is_superuser=True).all()

    # This test runs only for superuser creation, when no superuser registered
    if user.count() > 0:
        user[0].send_email(subject=subject, html_message=message)




class EmailToken(models.Model):
    """
    EmailToken is used for email verification & resetting password
    """
    class Meta:
        verbose_name = "Email Token"
        verbose_name_plural = "Email Tokens"

    token = models.CharField(default='', max_length=50)
    user = models.OneToOneField(User, blank=None, on_delete=models.CASCADE, unique=True)
    expiredAt = models.DateField(default=datetime.now)

    @classmethod
    def generate_token(cls, user: User) -> str:
        obj, _ = cls.objects.get_or_create(user=user)
        obj.token = PasswordResetTokenGenerator().make_token(user=user)
        obj.expiredAt = datetime.now() + timedelta(days=7)
        obj.save()
        return obj.token

    @classmethod
    def verify_user_by_token(cls, token: str) -> bool:
        """

        :param token:
        :return: True if email was verified successfully
        False is token was not found or expired
        """

        try:
            obj = EmailToken.objects.get(token=token)
        except EmailToken.DoesNotExist:
            return False

        check = PasswordResetTokenGenerator().check_token(user=obj.user, token=token)

        if not check:
            # remove expired token
            obj.delete()
            return False

        obj.user.authenficate_email()
        # Delete token cause it was used
        obj.delete()

        return True




