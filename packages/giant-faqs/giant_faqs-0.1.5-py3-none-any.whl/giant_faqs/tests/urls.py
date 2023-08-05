from django.urls import include, path

""""
Url patterns for testing
"""

urlpatterns = [path("faqs/", include("giant_faqs.urls", namespace="faqs"))]
