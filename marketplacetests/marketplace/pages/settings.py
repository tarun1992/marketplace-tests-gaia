# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By

from marketplacetests.marketplace.pages.base import BasePage


class Settings(BasePage):

    _page_loaded_locator = (By.CSS_SELECTOR, 'form.account-settings')

    _email_locator = (By.CSS_SELECTOR, '.settings-email.account-field > p')
    _sign_in_button_locator = (By.CSS_SELECTOR, 'a.button.login')
    _sign_out_button_locator = (By.CSS_SELECTOR, 'a.button.logout')

    def wait_for_sign_in_displayed(self):
        self.wait_for_element_displayed(*self._sign_in_button_locator)

    def wait_for_sign_out_button(self):
        self.wait_for_element_displayed(*self._sign_out_button_locator)

    def tap_sign_out(self):
        self.wait_for_sign_out_button()
        self.marionette.find_element(*self._sign_out_button_locator).tap()

    @property
    def email(self):
        return self.marionette.find_element(*self._email_locator).text
