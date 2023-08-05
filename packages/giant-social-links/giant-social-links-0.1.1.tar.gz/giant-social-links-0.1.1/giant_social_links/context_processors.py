from .models import SocialLink


def social_links(request):
    """
    Render the social media links from the SocialMedia model
    """
    return {
        "social_media_links": SocialLink.objects.enabled(),
    }
