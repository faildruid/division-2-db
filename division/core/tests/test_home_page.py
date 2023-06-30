"""Testing the home page."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse, resolve

from ..views import HomePageView
from .. import models

TEST_AUTH_PWD = "098y7ty3fgv45nj!ki90u8yu"


class HomepageTests(TestCase):
    """Tests for the home page."""

    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        """Check Status code."""
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        """Check file name."""
        self.assertTemplateUsed(self.response, "home.html")

    def test_homepage_contains_correct_html(self):
        """
        Check file contains the title ADR - Home.

        Validate that the html strings are at the start and the end of the rendered html
        """
        html = self.response.content.decode("utf8")
        self.assertTrue(html.startswith("<!doctype html>"))
        self.assertIn("<title>Division 2 Item DB - Home</title>", html)
        self.assertTrue(html.endswith("</html>"))

    def test_homepage_does_not_contain_incorrect_html(self):
        """Confirm a posited error code is not on the page."""
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_homepage_url_resolves_homepage_view(self):
        """Validate the homepage url."""
        view = resolve("/")
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)
