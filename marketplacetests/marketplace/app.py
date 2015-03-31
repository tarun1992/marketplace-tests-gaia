# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import By, expected, Wait
from marionette.keys import Keys
from gaiatest.apps.base import Base


class Marketplace(Base):

    # Default to the Dev app
    name = 'Marketplace'

    _marketplace_frame_locator = (By.CSS_SELECTOR, 'iframe[src*="marketplace"]')

    _body_loaded_locator = (By.CSS_SELECTOR, 'body.loaded')
    _loading_fragment_locator = (By.CSS_SELECTOR, 'div.loading-fragment')
    _offline_message_locator = (By.CSS_SELECTOR, 'div.error-message[data-l10n="offline"]')
    _settings_button_locator = (By.CSS_SELECTOR, '.act-tray.active .header-button.settings')
    _home_button_locator = (By.CSS_SELECTOR, 'h1.site a')
    _back_button_locator = (By.ID, 'nav-back')
    _notification_locator = (By.ID, 'notification-content')

    # Marketplace search on home page
    _search_locator = (By.ID, 'search-q')
    _signed_in_notification_locator = (By.CSS_SELECTOR, '#notification.show')

    # System app install notification message
    _install_notification_locator = (By.CSS_SELECTOR, '.banner.generic-dialog > p')

    def __init__(self, marionette, app_name=False):
        Base.__init__(self, marionette)
        if app_name:
            self.name = app_name
        self.manifest_url = "https://marketplace.firefox.com/app/965bbfd7-936d-451d-bebf-fafdc7ce8d9e/manifest.webapp"

    def launch(self, expect_success=True):
        Base.launch(self, launch_timeout=120000)
        self.wait_for_element_not_displayed(*self._loading_fragment_locator)
        if expect_success:
            self.switch_to_marketplace_frame()
            from marketplacetests.marketplace.regions.home import Home
            home_page = Home(self.marionette)
            return home_page

    def switch_to_marketplace_frame(self):
        self.marionette.switch_to_frame()
        self.wait_for_element_present(*self._marketplace_frame_locator)
        marketplace_frame = self.marionette.find_element(*self._marketplace_frame_locator)
        self.marionette.switch_to_frame(marketplace_frame)
        self.wait_for_element_present(*self._marketplace_frame_locator)
        marketplace_frame = self.marionette.find_element(*self._marketplace_frame_locator)
        self.marionette.switch_to_frame(marketplace_frame)

    def login(self, username, password):
        settings = self.tap_settings()
        ff_accounts = settings.tap_sign_in()
        ff_accounts.login(username, password)
        self.switch_to_marketplace_frame()
        self.wait_for_notification_message_displayed()
        self.wait_for_notification_message_not_displayed()
        return settings

    @property
    def offline_message_text(self):
        self.wait_for_element_displayed(*self._offline_message_locator)
        return self.marionette.find_element(*self._offline_message_locator).text

    def wait_for_notification_message_displayed(self, message=None):
        if message:
            Wait(marionette=self.marionette).until(
                lambda m: self.notification_message == message)
        self.wait_for_element_displayed(*self._notification_locator)

    def wait_for_notification_message_not_displayed(self):
        self.wait_for_element_not_displayed(*self._notification_locator)

    def wait_for_page_loaded(self):
        Wait(self.marionette).until(
            expected.element_present(*self._body_loaded_locator))
        Wait(self.marionette).until(
            expected.element_present(*self._page_loaded_locator))

    @property
    def notification_message(self):
        return self.marionette.find_element(*self._notification_locator).text

    def _perform_search(self, term):
        self.wait_for_page_loaded()
        search_box = Wait(self.marionette).until(
            expected.element_present(*self._search_locator))
        Wait(self.marionette).until(expected.element_displayed(search_box))
        search_box.send_keys(term)

        search_box.send_keys(Keys.RETURN)

    def search(self, term):
        self._perform_search(term)
        from marketplacetests.marketplace.regions.search_results import SearchResults
        return SearchResults(self.marionette)

    def set_region(self, region):
        self._perform_search(':debug')
        from marketplacetests.marketplace.regions.debug import Debug
        debug_screen = Debug(self.marionette)
        debug_screen.select_region(region)
        # wait for notification of the change
        self.wait_for_notification_message_displayed()
        if region not in self.notification_message:
            raise Exception('Unable to change region to %s. Notification displayed: %s'
                            % (region, self.notification_message))

        debug_screen.tap_back()

    def navigate_to_app(self, app_name):
        search_results = self.search(app_name).search_results
        for result in search_results:
            if result.name == app_name:
                return result.tap_app()

        # app not found
        raise Exception('The app: %s was not found.' % app_name)

    def tap_settings(self):
        self.wait_for_element_displayed(*self._settings_button_locator)
        self.marionette.find_element(*self._settings_button_locator).tap()
        from marketplacetests.marketplace.regions.settings import Settings
        return Settings(self.marionette)

    def tap_home(self):
        self.marionette.find_element(*self._home_button_locator).tap()

    def tap_back(self):
        self.marionette.find_element(*self._back_button_locator).tap()

    @property
    def install_notification_message(self):
        self.marionette.switch_to_frame()
        self.wait_for_element_displayed(*self._install_notification_locator)
        return self.marionette.find_element(*self._install_notification_locator).text
