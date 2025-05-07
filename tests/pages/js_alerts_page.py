from playwright.sync_api import Page

from framework.ui.decorators.decorators import step
from framework.ui.elements.button import Button
from framework.ui.elements.label import Label
from framework.ui.pages.base_page import BasePage


class JavaScriptAlertsPage(BasePage):

    def __init__(self, page: Page):
        header_locator = page.locator('h3:has-text("JavaScript Alerts")')
        super().__init__(page, header_locator, "JavaScript Alerts Page")

        self._js_alert_button = Button(page, page.locator('[onclick="jsAlert()"]'), "Click for JS Alerts Button")
        self._js_prompt_button = Button(page, page.locator('[onclick="jsPrompt()"]'), "Click for JS Alerts Button")
        self._result_message_lbl = Label(page, "#result", "Result TextBox")

    @step("Click the JS Alert button")
    def trigger_js_alert(self) -> None:
        self._js_alert_button.click()

    @step("Click the JS Prompt button")
    def trigger_js_prompt(self) -> None:
        self._js_prompt_button.click()

    @step("Get displayed Result message")
    def get_result_message(self) -> str:
        self._result_message_lbl.state.wait_for_displayed()
        result_msg = self._result_message_lbl.get_text()
        return result_msg
