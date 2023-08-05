from django.contrib.sitemaps import Sitemap

from .models import FAQ


class ArticleSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        """
        Get all published articles
        """
        return FAQ.objects.active()

    def lastmod(self, obj):
        return obj.updated_at
