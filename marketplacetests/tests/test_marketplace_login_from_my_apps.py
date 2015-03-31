# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceLoginFromMyApps(MarketplaceGaiaTestCase):

    def test_marketplace_sign_in_and_sign_out_from_my_apps(self):
        username = self.testvars['marketplace']['username']
        password = self.testvars['marketplace']['password']

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()

        settings = home_page.tap_settings()
        my_apps = settings.go_to_my_apps_page()

        self.assertEqual(my_apps.login_required_message, 'You must be signed in to view your apps.')
        ff_accounts = settings.tap_sign_in_from_my_apps()

        ff_accounts.login(username, password)

        # switch back to Marketplace
        marketplace.switch_to_marketplace_frame()
        my_apps.wait_for_notification_message_displayed()
        my_apps.wait_for_notification_message_not_displayed()

        self.wait_for_condition(lambda m: len(my_apps.my_apps_list) > 0)
        settings = my_apps.go_to_settings_page()

        # Sign out, which should return to the Marketplace home screen
        settings.tap_sign_out()

        # Verify that user is signed out
        settings.wait_for_sign_in_displayed()
