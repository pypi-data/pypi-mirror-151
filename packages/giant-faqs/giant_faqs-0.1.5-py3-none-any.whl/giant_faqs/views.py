from django.conf import settings
from django.views.generic import ListView

from . import models
from .forms import FAQSearchForm


class FAQIndex(ListView):
    """
    Index view for giant_faqs queryset
    """

    model = models.Category
    template_name = "faqs/index.html"

    def get_queryset(self):
        """
        Override get method here to allow us to filter using tags
        """
        queryset = models.Category.objects.all()
        if not settings.FAQ_SEARCH:
            return queryset

        form = FAQSearchForm(data=self.request.GET or None, queryset=queryset)
        if form.is_valid():
            return form.process()

    def get_initial(self):
        return {
            "search": self.request.GET.get("search"),
        }

    def get_context_data(self, **kwargs):
        """
        Update the context with extra args
        """

        context = {
            "is_qs_faq": True if self.object_list.model is models.FAQ else False,
            "faq_queryset": self.object_list,
            "form": FAQSearchForm(
                queryset=self.object_list, initial=self.get_initial()
            ) if settings.FAQ_SEARCH else None,
        }

        return context
