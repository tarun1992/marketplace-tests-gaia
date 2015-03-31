# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import Wait
from fxapom.fxapom import FxATestAccount

from marketplacetests.firefox_accounts.app import FirefoxAccounts
from marketplacetests.payment.app import Payment
from marketplacetests.in_app_payments.in_app import InAppPayment
from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase


class TestNotYouLinkInAppPayment(MarketplaceGaiaTestCase):

    def test_not_you_link_in_app_payment(self):

        self.app_name = 'Testing In-App-Payments'
        app_title = 'In-App-Payments'

        self.install_in_app_payments_test_app()

        # Verify that the app icon is visible on one of the homescreen pages
        self.assertTrue(
            self.homescreen.is_app_installed(self.app_name),
            'App %s not found on homescreen' % self.app_name)

        # Click icon and wait for h1 element displayed
        self.homescreen.installed_app(self.app_name).tap_icon()
        Wait(self.marionette).until(lambda m: m.title == app_title)

        acct = FxATestAccount(base_url=self.base_url).create_account()

        tester_app = InAppPayment(self.marionette)
        fxa = tester_app.tap_buy_product()
        fxa.login(acct.email, acct.password)

        payment = Payment(self.marionette)
        payment.tap_cancel_pin()

        tester_app.tap_buy_product()
        fxa = FirefoxAccounts(self.marionette)
        self.assertTrue(fxa.is_not_you_logout_link_visible)
        self.assertEqual('You are signed in as: %s' % acct.email, 'You are signed in as: %s' % fxa.email_text)

        fxa.tap_not_you()
        fxa.wait_for_password_field_visible()
