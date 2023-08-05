from django.db import models

from giant_plugins.utils import RichTextField
from mixins.models import TimestampMixin


class FAQQuerySet(models.QuerySet):
    """
    Custom queryset method to show non-hidden giant_faqs
    """

    def active(self, user=None):
        """
        Return the active queryset, or all if user is admin
        """
        if user and user.is_staff:
            return self.all()

        return self.filter(is_active=True)


class FAQ(TimestampMixin):
    """
    A single question/answer pair.
    """

    question = models.CharField(max_length=255)
    answer = RichTextField()
    category = models.ForeignKey(
        to="giant_faqs.Category",
        related_name="faqs",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=False, help_text="Check this to show FAQ on index page"
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Higher number means a higher priority in listing."
    )

    objects = FAQQuerySet.as_manager()

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ["-order", "question"]

    def __str__(self):
        return self.question


class Category(models.Model):
    """
    Model for storing a FAQ Category in the database
    """

    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(
        default=0, help_text="Higher number means a higher priority in listing."
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
