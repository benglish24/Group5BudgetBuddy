"""Tests."""
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from users.models import CustomUser


# Create your tests here.
class SignUpViewTestCase(TestCase):
    """Tests for `SignUpView` view."""

    @parameterized.expand(
        [
            # Test case succeeds because of strong password
            (
                {
                    "first_name": "john",
                    "last_name": "doe",
                    "email": "jdoe@gmail.com",
                    "password1": "p@$$W0RDL@rG3",
                    "password2": "p@$$W0RDL@rG3",
                },
                # successful registrion should redirect (HTTP 302) to login page
                HTTPStatus.FOUND,
            ),
            # Test case fails because of weak password
            (
                {
                    "first_name": "john",
                    "last_name": "doe",
                    "email": "jdoe@gmail.com",
                    "password1": "password",
                    "password2": "password",
                },
                HTTPStatus.OK,
            ),
        ]
    )
    def test_signup_view(self, params, status_code):
        """Test `SignUpView` with strong and weak passwords.

        Tests if registration is successful for strong passwords.
        Tests if registration fails for weak passwords.

        """
        signup_url = reverse("users:signup")
        response = self.client.post(signup_url, data=params)
        self.assertEqual(response.status_code, status_code)


class LoginTestCase(TestCase):
    """Tests for Django's built-in `Login` view."""

    def setUp(self):
        """Set up test data for the class."""
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

        self.login_params = {"username": "jdoe@gmail.com", "password": "p@$$W0RDL@rG3"}
        CustomUser.objects.create_user(email="jdoe@gmail.com", password="p@$$W0RDL@rG3")

    def test_loginview(self):
        """Test `LoginView`, it should redirect."""
        response = self.client.post(self.login_url, data=self.login_params)
        # redirects after a successful login
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.get(reverse("polls:question-list"))
        self.assertEqual(str(response.context.get("user")), "jdoe@gmail.com")

    def test_logged_in_user_sees_correct_template(self):
        """Test if logged in user sees the password change page."""
        response = self.client.login(email="jdoe@gmail.com", password="p@$$W0RDL@rG3")
        response = self.client.get(reverse("password_change"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_anonymous_user_sees_correct_template(self):
        """Test not logged in user should not see password change page."""
        response = self.client.get(reverse("password_change"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_signinview_invalid_user_password(self):
        """Test login by providing invalid user credentials."""
        response = self.client.post(
            self.login_url, data={"username": "jdoe@gmail.com", "password": "password"}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "registration/login.html")
        self.assertTrue("errors" in response.context)
        self.assertTrue(
            "Please enter a correct email address and password"
            in str(response.context.get("errors"))
        )
        self.assertEqual(str(response.context.get("user")), "AnonymousUser")

    def test_login_and_logout(self):
        """Test logout by login in first and then logout.

        Tests when a user logs out, the `user` object in the `Response` is "AnyonymousUser".

        """
        response = self.client.post(self.login_url, data=self.login_params)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        response = self.client.get(reverse("polls:question-list"))
        self.assertEqual(str(response.context.get("user")), "jdoe@gmail.com")

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        response = self.client.get(reverse("polls:question-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(str(response.context.get("user")), "AnonymousUser")
