import json
import logging
import os
from enum import Enum
from pathlib import Path
from typing import Dict

import allure
from allure_commons.types import AttachmentType
from behave import use_fixture
from behave.model_core import Status
from playwright.sync_api import sync_playwright

from configs.settings import DEFAULT_CONFIGURATION_FILE
from framework.logger import logger
from framework.ui.browser.browser import Browser
from framework.ui.browser.window import DEFAULT_VIEWPORT_SIZE
from framework.ui.constants.timeouts import WaitTimeoutsMs
from tests.fixtures import register_dialog_handler

PROJECT_ROOT_DIR = Path(__file__).parent.parent.resolve()

FIXTURES = {
    "register_dialog_handler": register_dialog_handler,
}


class BrowserType(Enum):
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


def _get_browser(playwright: sync_playwright, browser_type: BrowserType, headless: bool = False) -> Browser:
    browser_map = {
        BrowserType.FIREFOX: playwright.firefox,
        BrowserType.WEBKIT: playwright.webkit,
        BrowserType.CHROMIUM: playwright.chromium
    }
    browser = browser_map.get(browser_type, playwright.chromium)
    browser_instance = browser.launch(headless=headless)
    context = browser_instance.new_context(viewport=DEFAULT_VIEWPORT_SIZE)
    context.set_default_timeout(WaitTimeoutsMs.WAIT_PAGE_LOAD)

    page = context.new_page()

    custom_browser = Browser(page)
    return custom_browser


def before_all(context):
    """Setup environment before all tests (similar to pytest_configure)."""
    allure_dir = PROJECT_ROOT_DIR.joinpath(context.config.userdata.get("allure_report_dir", "allure-results")).resolve()
    os.makedirs(allure_dir, exist_ok=True)

    userdata = context.config.userdata
    context.browser_type = userdata.get('browser', BrowserType.CHROMIUM.value)
    context.headless = userdata.getbool('headless', False)
    config_file = userdata.get('config', DEFAULT_CONFIGURATION_FILE)

    logger.setup_logger()
    logging.info("Test logging successfully configured for test execution.")

    context.test_config = parse_config(config_file)


def before_feature(context, feature):
    """Setup environment before each feature."""
    context.playwright = sync_playwright().start()
    context.browser = _get_browser(
        context.playwright,
        BrowserType(context.browser_type),
        context.headless
    )
    for tag in feature.tags:
        use_fixture_by_tag(tag, context)


def after_feature(context, feature):
    if hasattr(context, 'browser') and context.browser:
        context.browser.page.close()
        context.browser.page.context.browser.close()

    if hasattr(context, 'playwright') and context.playwright:
        context.playwright.stop()


def before_scenario(context, scenario):
    """Setup environment before each scenario.    """
    for tag in scenario.tags:
        use_fixture_by_tag(tag, context)


def after_step(context, step):
    if step.status == Status.failed:
        if hasattr(context, "browser") and context.browser:
            allure.attach(
                context.browser.page.screenshot(),
                name="Screenshot",
                attachment_type=AttachmentType.PNG
            )


def parse_config(config_path: str = DEFAULT_CONFIGURATION_FILE) -> Dict[str, str]:
    """Parse the configuration file."""
    config_path = PROJECT_ROOT_DIR.joinpath(config_path).resolve()
    try:
        with open(config_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise Exception(f"Configuration file not found at: {config_path}")
    return data


def use_fixture_by_tag(tag, context):
    # Accordingly Naming Convention for Fixture Tags,
    # fixture tags should start with "@fixture.*" prefix to improve readability in feature files

    fixture_prefix = "fixture."
    if tag.startswith(fixture_prefix):
        fixture_name = tag[len(fixture_prefix):]
        fixture_func = FIXTURES.get(fixture_name)
        if fixture_func:
            use_fixture(fixture_func, context)
        else:
            logging.warning(f"Fixture '{fixture_name}' is not registered")
