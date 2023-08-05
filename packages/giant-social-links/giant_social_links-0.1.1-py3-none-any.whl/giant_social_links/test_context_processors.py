from django.test import RequestFactory

import pytest

from .context_processors import social_links
from .models import SocialLink


@pytest.mark.django_db
class TestContextProcessor:
    @pytest.fixture
    def enabled_link(self):
        return SocialLink.objects.create(
            name="enabled",
            url="enabled.com",
            is_enabled=True)

    @pytest.fixture
    def disabled_link(self):
        return SocialLink.objects.create(
            name="disabled",
            url="disabled.com",
            is_enabled=False,
        )

    def test_enabled_social_links_only(self, enabled_link, disabled_link):
        dict = social_links(RequestFactory())
        social_link_queryset = dict["social_media_links"]
        assert (
                len(social_link_queryset) == 1 and
                social_link_queryset.first().name == enabled_link.name
        )
