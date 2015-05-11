# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By

from marketplacetests.marketplace.pages.base import BasePage
from marketplacetests.marketplace.pages.app_details import Details


class AddReview(BasePage):
    """
    Page for adding reviews.
    """

    _page_loaded_locator = (By.CSS_SELECTOR, 'form.add-review-form')

    _add_review_input_field_locator = (By.ID, 'review-body')
    _submit_review_button_locator = (By.CSS_SELECTOR, 'button[type="submit"]')
    _rating_locator = (By.CSS_SELECTOR, ".ratingwidget.stars-0 > label[data-stars='%s']")

    def set_review_rating(self, rating):
        self.marionette.find_element(self._rating_locator[0], self._rating_locator[1] % rating).tap()

    def type_review(self, text):
        self.marionette.find_element(*self._add_review_input_field_locator).send_keys(text)

    def write_a_review(self, rating, body):
        self.set_review_rating(rating)
        self.type_review(body)
        submit_button = self.marionette.find_element(*self._submit_review_button_locator)
        # This workaround is required for gaia v2.0, but can be removed in later versions
        # as the bug has been fixed
        # Bug 937053 - tap() method should calculate elementInView from the coordinates of the tap
        self.marionette.execute_script('arguments[0].scrollIntoView(false);', [submit_button])
        submit_button.tap()
        return Details(self.marionette)
