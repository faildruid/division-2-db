""" Core Views"""

from django.views.generic import TemplateView

class HomePageView(TemplateView):
    """About page View."""

    template_name = "home.html"
