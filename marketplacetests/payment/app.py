# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from gaiatest.apps.base import Base
from marionette import expected, By, Wait

from marketplacetests.marketplace.app import Marketplace


class Payment(Marketplace):

    _payment_frame_locator = (By.CSS_SELECTOR, "#trustedui-frame-container > iframe")

    _loading_throbber_locator = (By.CSS_SELECTOR, '.loading')

    # Create/confirm PIN
    _pin_container_locator = (By.CSS_SELECTOR, '.pinbox')
    _pin_digit_holder_locator = (By.CSS_SELECTOR, '.pinbox span')
    _pin_continue_button_locator = (By.CSS_SELECTOR, '.cta')
    _pin_heading_locator = (By.CSS_SELECTOR, 'section.content h1')
    _pin_error_locator = (By.CSS_SELECTOR, 'section.content p.err-msg')
    _forgot_pin_locator = (By.CSS_SELECTOR, 'p.forgot-pin a')
    _cancel_pin_button_locator = (By.CSS_SELECTOR, '.button.cancel')
    _reset_pin_button_locator = (By.XPATH, "//button[text()='Reset']")

    # Final buy app panel
    _app_name_locator = (By.CSS_SELECTOR, '.product .title')
    _buy_button_locator = (By.XPATH, "//button[text()='Buy']")
    _cancel_button_locator = (By.CSS_SELECTOR, '.buttons button.cancel')
    _confirm_payment_header_locator = (By.CSS_SELECTOR, 'main > h1')
    _in_app_product_name_locator = (By.CSS_SELECTOR, '.title')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.switch_to_payment_frame()

    def switch_to_payment_frame(self):
        self.marionette.switch_to_frame()
        self.wait_for_element_present(*self._payment_frame_locator)
        payment_iframe = self.marionette.find_element(*self._payment_frame_locator)
        self.marionette.switch_to_frame(payment_iframe)

    @property
    def app_name(self):
        return self.marionette.find_element(*self._app_name_locator).text

    @property
    def in_app_product_name(self):
        return self.marionette.find_element(*self._in_app_product_name_locator).text

    @property
    def confirm_payment_header_text(self):
        self.wait_for_buy_app_section_displayed()
        return self.marionette.find_element(*self._confirm_payment_header_locator).text

    @property
    def pin_heading(self):
        return self.marionette.find_element(*self._pin_heading_locator).text

    @property
    def pin_error(self):
        self.wait_for_element_displayed(*self._pin_error_locator)
        return self.marionette.find_element(*self._pin_error_locator).text

    def create_pin(self, pin):
        element = Wait(self.marionette).until(
            expected.element_present(*self._pin_container_locator))
        Wait(self.marionette).until(
            expected.element_displayed(element))
        Wait(self.marionette).until(lambda m: 'Create' in self.pin_heading)
        self.keyboard.send(pin)
        self.switch_to_payment_frame()
        self.tap_pin_continue()
        self.confirm_pin(pin)

    def confirm_pin(self, pin):
        Wait(self.marionette).until(lambda m: 'Confirm' in self.pin_heading)
        element = Wait(self.marionette).until(
            expected.element_present(*self._pin_container_locator))
        Wait(self.marionette).until(
            expected.element_displayed(element))
        # We need to click() on the pin container to display the keyboard
        # a tap() does not work
        element.click()
        self.keyboard.send(pin)
        self.switch_to_payment_frame()
        self.tap_pin_continue()

    def enter_pin(self, pin):
        element = Wait(self.marionette).until(
            expected.element_present(*self._pin_container_locator))
        Wait(self.marionette).until(
            expected.element_displayed(element))
        Wait(self.marionette).until(lambda m: 'PIN' in self.pin_heading)
        self.keyboard.send(pin)
        self.switch_to_payment_frame()
        self.tap_pin_continue()

    def tap_cancel_pin(self):
        self.wait_for_element_displayed(*self._cancel_pin_button_locator)
        self.marionette.find_element(*self._cancel_pin_button_locator).tap()
        self.apps.switch_to_displayed_app()

    def tap_pin_continue(self):
        button = Wait(self.marionette).until(
            expected.element_present(*self._pin_continue_button_locator))
        Wait(self.marionette).until(expected.element_displayed(button))
        Wait(self.marionette).until(expected.element_enabled(button))
        button.tap()

    def wait_for_buy_app_section_displayed(self):
        self.wait_for_element_displayed(*self._buy_button_locator)

    def tap_buy_button(self):
        self._tap_payment_button(self._buy_button_locator)

    def tap_forgot_pin(self):
        self.wait_for_element_displayed(*self._forgot_pin_locator)
        self.marionette.find_element(*self._forgot_pin_locator).tap()

    def tap_reset_button(self):
        button = Wait(self.marionette).until(
            expected.element_present(*self._reset_pin_button_locator))
        Wait(self.marionette).until(expected.element_displayed(button))
        Wait(self.marionette).until(expected.element_enabled(button))
        # This workaround is required for gaia v2.0, but can be removed in later versions
        # as the bug has been fixed
        # Bug 937053 - tap() method should calculate elementInView from the coordinates of the tap
        self.marionette.execute_script('arguments[0].scrollIntoView(false);', [button])
        button.tap()

    def tap_cancel_button(self):
        self._tap_payment_button(self._cancel_button_locator)

    def _tap_payment_button(self, button_locator):
        self.marionette.switch_to_frame()
        self.wait_for_element_not_displayed(*self._loading_throbber_locator)
        payment_iframe = self.marionette.find_element(*self._payment_frame_locator)
        self.marionette.switch_to_frame(payment_iframe)
        self.wait_for_element_displayed(*button_locator)
        self.marionette.find_element(*button_locator).tap()
        self.marionette.switch_to_frame()
        self.wait_for_element_not_present(*self._payment_frame_locator)
        self.return_to_app()

    def return_to_app(self):
        self.switch_to_marketplace_frame()


class InAppPayment(Payment):

    def return_to_app(self):
        self.apps.switch_to_displayed_app()
