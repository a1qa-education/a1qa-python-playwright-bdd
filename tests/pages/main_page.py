import logging
from enum import Enum

from playwright.sync_api import Page

from framework.ui.constants.elements import LocatorTemplates
from framework.ui.elements.label import Label
from framework.ui.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class MainPageNavigation(Enum):

    BASIC_AUTH = ("/basic_auth", "Basic Auth")
    DYNAMIC_CONTROLS = ("/dynamic_controls", "Dynamic Controls")
    FILE_DOWNLOAD = ("/download", "File Download")
    FILE_UPLOAD = ("/upload", "File Upload")
    FRAMES = ("/forms", "Frames")
    JAVASCRIPT_ALERTS = ("/javascript_alerts", "JavaScript Alerts")
    SORTABLE_DATA_TABLES = ("/tables", "Sortable Data Tables")

    def __init__(self, path: str, display_name: str):
        self.path = path
        self.display_name = display_name


class MainPage(BasePage):

    def __init__(self, page: Page):
        header_locator = page.locator(LocatorTemplates.HEADER_BY_TEXT.format(text="Welcome to the-internet"))
        super().__init__(page, header_locator, "The-internet Main Page")

    def click_navigation_link(self, navigation: MainPageNavigation) -> None:
        """
        Clicks on the navigation link to open the corresponding page.

        :param navigation: Navigation enum with path and display name.
        """
        logger.info(f"Click navigation link: '{navigation.display_name}'")
        link = self._get_page_link(navigation.path, navigation.display_name)
        link.click()

    def _get_page_link(self, path: str, name: str) -> Label:
        return Label(self.page, LocatorTemplates.LINK_BY_TEXT.format(text=path), f"{name} Link")
