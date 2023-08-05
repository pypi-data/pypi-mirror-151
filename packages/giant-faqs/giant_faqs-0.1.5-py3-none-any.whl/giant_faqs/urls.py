from django.urls import path

from .views import FAQIndex

app_name = "giant_faqs"

urlpatterns = [
    path("", FAQIndex.as_view(), name="index"),
]
