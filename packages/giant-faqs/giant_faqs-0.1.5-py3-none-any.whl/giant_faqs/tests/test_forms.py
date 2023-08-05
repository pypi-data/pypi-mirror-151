import pytest

from giant_faqs import forms, models


@pytest.mark.django_db
class TestFAQSearchForm:
    @pytest.fixture
    def form(self, mocker):
        return forms.FAQSearchForm(queryset=mocker.Mock())

    def test_filter_by_valid_search_term(self, shown_faq):
        data = {
            "search": "that",
        }
        form = forms.FAQSearchForm(queryset=models.FAQ.objects.all(), data=data)
        form.is_valid()

        results = form.process()
        expected_count_of_faqs_in_results = 1
        result = results.first()
        faqs = models.FAQ.objects.active().filter(question__icontains=data["search"])

        assert results.count() == expected_count_of_faqs_in_results
        assert result in faqs

    def test_filter_by_invalid_search_term(self, shown_faq):
        data = {
            "search": "invalid",
        }
        form = forms.FAQSearchForm(queryset=models.FAQ.objects.all(), data=data)
        form.is_valid()

        results = form.process()
        expected_count_of_faqs_in_results = 0

        assert results.count() == expected_count_of_faqs_in_results

    def test_filter_with_no_search_term(self, shown_faq):
        data = {
            "search": "",
        }
        form = forms.FAQSearchForm(queryset=models.FAQ.objects.all(), data=data)
        form.is_valid()

        results = form.process()
        expected_count_of_faqs_in_results = 1

        assert results.count() == expected_count_of_faqs_in_results
