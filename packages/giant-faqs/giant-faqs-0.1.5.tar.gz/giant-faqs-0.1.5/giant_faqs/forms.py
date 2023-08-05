from django import forms

from . import models


class FAQSearchForm(forms.Form):
    """
    Form to provide search filtering for giant_faqs.
    """

    search = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Search for a FAQ", "title": "Search FAQs"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.queryset = kwargs.pop("queryset")
        super().__init__(*args, **kwargs)

    def process(self):
        """
        Filter the queryset based on search entry
        """

        search_query = self.cleaned_data.get("search")
        relevant_search_faqs = self.queryset

        if not search_query:
            return relevant_search_faqs
        else:
            faq_qs = models.FAQ.objects.active()
            relevant_search_faqs = faq_qs.filter(question__icontains=search_query)

        return relevant_search_faqs
