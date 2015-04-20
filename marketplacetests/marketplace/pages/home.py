# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By

from marketplacetests.marketplace.pages.base import BasePage


class Home(BasePage):

    _page_loaded_locator = (By.CSS_SELECTOR, 'div.feed-home')
