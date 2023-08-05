from django.db import models

from filer.fields.image import FilerImageField
from mixins.models import TimestampMixin


class SocialLinkQuerySet(models.QuerySet):
    """
    Custom queryset class for the Link class
    """

    def enabled(self):
        """
        Shows only the Link objects with is_enabled=True
        """
        return self.filter(is_enabled=True)


class SocialLink(TimestampMixin):
    """
    Represents a Social Media object which will be displayed
    in the footer. Contains a link, name and image field.
    """

    name = models.CharField(max_length=255)
    url = models.URLField()
    icon = FilerImageField(related_name="links", on_delete=models.SET_NULL, blank=True, null=True)
    order = models.PositiveIntegerField(
        default=0,
        help_text="Set this to prioritise the order of the icon, higher numbers are shown first.",
    )
    is_enabled = models.BooleanField(
        default=False, help_text="Check this if you would like this icon to be displayed."
    )

    objects = SocialLinkQuerySet.as_manager()

    class Meta:
        ordering = ["-order", "name", "-created_at"]

    def __str__(self) -> str:
        return self.name
