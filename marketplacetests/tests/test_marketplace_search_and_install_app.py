# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.homescreen.app import Homescreen
from gaiatest.apps.homescreen.regions.confirm_install import ConfirmInstall
from marionette.by import By

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestSearchMarketplaceAndInstallApp(MarketplaceGaiaTestCase):

    def test_search_and_install_app(self):

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()

        popular_apps_page = home_page.popular_apps_page
        app_name = popular_apps_page.popular_apps[0].name
        app_author = popular_apps_page.popular_apps[0].author

        # Remove the app if already installed
        if self.apps.is_app_installed(app_name):
            self.apps.kill(marketplace.app)
            self.apps.uninstall(app_name)
            home_page = marketplace.launch()
            popular_apps_page = home_page.popular_apps_page

        marketplace.switch_to_marketplace_frame()

        results = popular_apps_page.search(app_name)

        self.assertGreater(len(results.search_results), 0, 'No results found.')

        first_result = results.search_results[0]

        self.assertEquals(first_result.name, app_name, 'First app has the wrong name.')
        self.assertEquals(first_result.author, app_author, 'First app has the wrong author.')

        # Find and click the install button to the install the web app
        self.assertEquals(first_result.install_button_text, 'Free', 'Incorrect button label.')

        first_result.tap_install_button()
        self.wait_for_downloads_to_finish()

        # Confirm the installation and wait for the app icon to be present
        confirm_install = ConfirmInstall(self.marionette)
        confirm_install.tap_confirm()

        self.assertEqual('%s installed' % app_name, results.install_notification_message)

        # Press Home button
        self.device.touch_home_button()

        # Check that the icon of the app is on the homescreen
        homescreen = Homescreen(self.marionette)
        self.apps.switch_to_displayed_app()

        self.assertTrue(homescreen.is_app_installed(app_name))
