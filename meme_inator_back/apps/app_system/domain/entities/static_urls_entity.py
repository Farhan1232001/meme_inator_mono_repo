
from dataclasses import dataclass
from typing import Optional
from core.constants.app_sys_constants import (
    APP_NAME, APP_VERSION, 
    APP_ICON_URL, FAQ_PAGE_URL, TERMS_OF_SERVICE_URL, 
    PRIVACY_POLICY_URL, CONTACT_SUPPORT_URL
)

@dataclass
class StaticUrlsEntity:
    faq_url: str
    contact_support_url: str
    privacy_policy_url: str
    terms_of_service_url: str

    def get_url(self, url_type: str):
        """
        Retrieves a specific predefined URL based on the provided URL type identifier.

        The function accepts both short-form and long-form string identifiers for common URLs.

        Args:
            url_type: A string identifier for the desired URL.
                    Supported values:
                    - 'faq' or 'frequently_asked_questions': For the Frequently Asked Questions page.
                    - 'cs' or 'contact_support': For the Contact Support page.
                    - 'pp' or 'privacy_policy': For the Privacy Policy page.
                    - 'tos' or 'terms_of_service': For the Terms of Service page.

        Returns:
            The corresponding URL string, which is assumed to be defined elsewhere
            as global constants (e.g., FAQ_PAGE_URL).
        """
        match url_type:
            # optimized
            case 'faq': return FAQ_PAGE_URL
            case 'cs': return CONTACT_SUPPORT_URL
            case 'pp': return PRIVACY_POLICY_URL
            case 'tos': return TERMS_OF_SERVICE_URL
            # not optimized
            case 'frequently_asked_questions': return FAQ_PAGE_URL
            case 'contact_support':
                return CONTACT_SUPPORT_URL
            case 'privacy_policy':
                return PRIVACY_POLICY_URL
            case 'terms_of_service':
                return TERMS_OF_SERVICE_URL
                

    # Setters, NOT IN USE
    # To set urls, go to core/constants/app_sys_constants.py
    def set_faq_url(self, url: str):
        raise NotImplementedError

    def set_contact_support_url(self, url: str):
        raise NotImplementedError

    def set_privacy_policy_url(self, url: str):
        raise NotImplementedError

    def set_terms_ofservice_url(self, url: str):
        raise NotImplementedError
