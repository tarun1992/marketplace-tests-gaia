# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from gaiatest.apps.base import Base
from marionette import expected, By, Wait


class Payment(Base):

    _payment_frame_locator = (By.CSS_SELECTOR, "#trustedui-frame-container > iframe")

    _loading_throbber_locator = (By.CSS_SELECTOR, '.loading')

    # Create/confirm PIN
    _pin_container_locator = (By.CSS_SELECTOR, '.pinbox')
    _pin_digit_holder_locator = (By.CSS_SELECTOR, '.pinbox span')
    _pin_continue_button_locator = (By.CSS_SELECTOR, '.cta')
    _pin_heading_locator = (By.CSS_SELECTOR, 'section.content h1')
    _cancel_pin_button_locator = (By.CSS_SELECTOR, '.button.cancel')

    # Final buy app panel
    _app_name_locator = (By.CSS_SELECTOR, '.product .title')
    _buy_button_locator = (By.XPATH, "//button[text()='Buy']")
    _cancel_button_locator = (By.XPATH, "//button[text()='Cancel']")
    _confirm_payment_header_locator = (By.CSS_SELECTOR, 'main > h1')
    _in_app_product_name_locator = (By.CSS_SELECTOR, '.title')
    _in_app_confirm_buy_button_locator = (By.ID, 'uxBtnBuyNow')

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
        Wait(self.marionette).until(lambda m: 'Enter' in self.pin_heading)
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
        self.marionette.switch_to_frame()
        self.wait_for_element_not_displayed(*self._loading_throbber_locator)
        payment_iframe = self.marionette.find_element(*self._payment_frame_locator)
        self.marionette.switch_to_frame(payment_iframe)
        if self.is_element_present(*self._buy_button_locator):
            self.marionette.find_element(*self._buy_button_locator).tap()
        else:
            self.marionette.find_element(*self._in_app_confirm_buy_button_locator).tap()
        self.marionette.switch_to_frame()
        self.wait_for_element_not_present(*self._payment_frame_locator)
        self.apps.switch_to_displayed_app()
