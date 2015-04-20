# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By

from marketplacetests.marketplace.pages.base import BasePage


class Feedback(BasePage):

    _page_loaded_locator = (By.CSS_SELECTOR, 'form.feedback-form')

    _feedback_textarea_locator = (By.NAME, 'feedback')
    _feedback_submit_button_locator = (By.CSS_SELECTOR, 'button[type="submit"]')

    def enter_feedback(self, feedback_text):
        feedback = self.marionette.find_element(*self._feedback_textarea_locator)
        feedback.clear()
        feedback.send_keys(feedback_text)
        self.switch_to_marketplace_frame()

    def submit_feedback(self):
        self.wait_for_element_displayed(*self._feedback_submit_button_locator)
        self.marionette.find_element(*self._feedback_submit_button_locator).tap()

    def wait_for_feedback_submitted_notification(self):
        self.wait_for_notification_message('Feedback submitted. Thanks!')
