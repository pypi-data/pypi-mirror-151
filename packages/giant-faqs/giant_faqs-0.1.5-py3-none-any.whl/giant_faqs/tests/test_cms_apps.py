from giant_faqs.cms_apps import FAQsApp


class TestFAQsApp:
    """
    Test case for the FAQsApp
    """

    def test_get_urls_method(self):
        """
        Test get_urls method on the FAQsApp class
        """
        assert FAQsApp().get_urls() == ["giant_faqs.urls"]
