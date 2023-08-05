import pytest

from giant_faqs.models import FAQ


@pytest.mark.django_db
class TestFAQQuerySet:
    """
    Test case for the FAQQuerySet class
    """

    def test_active_queryset(self, hidden_faq, shown_faq):
        """
        Test that the .published method returns the correct queryset objects
        """

        expected_number_of_objects = 1
        assert FAQ.objects.active().count() == expected_number_of_objects
        assert shown_faq in FAQ.objects.active()
        assert hidden_faq not in FAQ.objects.active()
