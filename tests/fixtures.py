from behave import fixture


@fixture
def register_dialog_handler(context):
    context.browser.dialog.register_dialog_handler(context.browser.dialog.accept)
    yield
