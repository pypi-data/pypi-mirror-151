from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class FAQsApp(CMSApp):
    """
    App hook for FAQs app
    """

    app_name = "faqs"
    name = "FAQs"

    def get_urls(self, page=None, language=None, **kwargs):
        """
        Return the path to the apps urls module
        """

        return ["giant_faqs.urls"]
