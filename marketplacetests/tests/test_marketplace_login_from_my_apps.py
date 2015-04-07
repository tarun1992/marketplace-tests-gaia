# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from fxapom.fxapom import FxATestAccount
from gaiatest.apps.homescreen.regions.confirm_install import ConfirmInstall

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceLoginFromMyApps(MarketplaceGaiaTestCase):

    def test_marketplace_sign_in_and_sign_out_from_my_apps(self):
        acct = FxATestAccount(base_url=self.base_url).create_account()

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()

        # We need to install an app first
        popular_apps_page = home_page.popular_apps_page
        self.app_name = popular_apps_page.popular_apps[0].name

        if self.apps.is_app_installed(self.app_name):
            raise Exception('The app %s is already installed.' % self.app_name)

        # Install the app
        marketplace.switch_to_marketplace_frame()
        settings = popular_apps_page.login(acct.email, acct.password)
        details_page = settings.navigate_to_app(self.app_name)
        details_page.tap_install_button()
        self.wait_for_downloads_to_finish()

        # Confirm the installation and wait for the app icon to be present
        confirm_install = ConfirmInstall(self.marionette)
        confirm_install.tap_confirm()
        self.assertEqual('%s installed' % self.app_name, details_page.install_notification_message)

        # Kill and restart marketplace
        self.apps.kill(marketplace.app)
        home_page = marketplace.launch()

        settings = home_page.tap_settings()
        settings.tap_sign_out()
        settings.wait_for_sign_in_displayed()

        my_apps = settings.go_to_my_apps_page()

        self.assertEqual(my_apps.login_required_message, 'You must be signed in to view your apps.')
        ff_accounts = settings.tap_sign_in_from_my_apps()

        ff_accounts.login(acct.email, acct.password)

        # switch back to Marketplace
        marketplace.switch_to_marketplace_frame()
        my_apps.wait_for_login_success_notification()

        self.wait_for_condition(lambda m: len(my_apps.my_apps_list) > 0)
        settings = my_apps.go_to_settings_page()

        # Sign out, which should return to the Marketplace home screen
        settings.tap_sign_out()

        # Verify that user is signed out
        settings.wait_for_sign_in_displayed()

    def tearDown(self):
        self.apps.uninstall(self.app_name)
        MarketplaceGaiaTestCase.tearDown(self)
