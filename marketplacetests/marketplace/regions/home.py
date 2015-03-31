# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By

from marketplacetests.marketplace.app import Marketplace
from marketplacetests.marketplace.regions.search_results import Result


class Home(Marketplace):

    _page_loaded_locator = (By.CSS_SELECTOR, 'div.feed-home')

    _popular_apps_tab_locator = (By.CSS_SELECTOR, 'a[href="/popular"]')

    def __init__(self, marionette):
        Marketplace.__init__(self, marionette)
        self.wait_for_page_loaded()

    @property
    def popular_apps_page(self):
        self.wait_for_element_displayed(*self._popular_apps_tab_locator)
        self.marionette.find_element(*self._popular_apps_tab_locator).tap()
        return PopularApps(self.marionette)


class PopularApps(Marketplace):

    _page_loaded_locator = (By.CSS_SELECTOR, 'ul.app-list')

    _gallery_apps_locator = (By.CSS_SELECTOR, '.app-list-app')

    def __init__(self, marionette):
        Marketplace.__init__(self, marionette)
        self.wait_for_page_loaded()

    @property
    def popular_apps(self):
        return [Result(self.marionette, app) for app in self.marionette.find_elements(*self._gallery_apps_locator)]
