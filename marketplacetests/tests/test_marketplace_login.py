# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from fxapom.fxapom import FxATestAccount

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceLogin(MarketplaceGaiaTestCase):

    def test_login_marketplace(self):
        # https://moztrap.mozilla.org/manage/case/4134/
        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()

        acct = FxATestAccount(base_url=self.base_url).create_account()

        settings = home_page.tap_settings()
        ff_accounts = settings.tap_sign_in()

        ff_accounts.login(acct.email, acct.password)

        # switch back to Marketplace
        marketplace.switch_to_marketplace_frame()

        # wait for signed-in notification at the bottom of the screen to clear
        settings.wait_for_sign_out_button()
        settings.wait_for_notification_message_not_displayed()

        # Verify that user is logged in
        self.assertEqual(acct.email, settings.email)

        # Sign out, which should return to the Marketplace home screen
        settings.tap_sign_out()

        # Verify that user is signed out
        settings.wait_for_sign_in_displayed()
