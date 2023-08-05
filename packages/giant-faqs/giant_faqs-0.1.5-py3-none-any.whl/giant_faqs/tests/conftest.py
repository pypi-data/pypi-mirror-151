import pytest

from giant_faqs.models import FAQ, Category


@pytest.fixture
def hidden_faq():
    return FAQ.objects.create(
        question="what is this?",
        answer="something",
        category=Category.objects.create(name="A"),
        is_active=False,
    )


@pytest.fixture
def shown_faq():
    return FAQ.objects.create(
        question="what is that?",
        answer="something else",
        category=Category.objects.create(name="B"),
        is_active=True,
    )
