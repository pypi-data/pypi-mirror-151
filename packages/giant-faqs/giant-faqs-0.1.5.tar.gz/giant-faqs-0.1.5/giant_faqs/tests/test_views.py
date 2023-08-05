from django.test import RequestFactory

import pytest

from giant_faqs.views import FAQIndex


@pytest.mark.django_db
class TestFAQView:
    """
    Test case for the FAQ app views
    """

    def test_get_context(self, shown_faq, hidden_faq):
        """
        Test the context update returns published giant_faqs queryset
        """

        form = {"search": "that"}
        view = FAQIndex()
        view.request = RequestFactory()
        view.request.GET = form

        view.object_list = view.get_queryset()
        context = view.get_context_data()

        assert shown_faq in context["faq_queryset"]
        assert hidden_faq not in context["faq_queryset"]
        assert context["is_qs_faq"]
