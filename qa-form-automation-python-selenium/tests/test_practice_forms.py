import unittest
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException


URL = "https://www.qapractice.com/practice-forms"

TEST_DATA = {
    "country": "India",
    "title": "Dr.",
    "first_name": "Ada",
    "last_name": "Lovelace",
    "dob": "1990-05-20",
    "doj": "01/06/2021",
    "email": "crao78689@gmail.com",
    "phone_code": "+91",
    "phone_number": "9876543210"
}


class PracticeFormsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()

        if os.getenv("HEADLESS", "1") != "0":
            options.add_argument("--headless=new")

        options.add_argument("--window-size=1440,1100")
        cls.driver = webdriver.Chrome(options=options)
        cls.wait = WebDriverWait(cls.driver, 15)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get(URL)

        self.wait.until(
            lambda driver: driver.execute_script(
                "return document.readyState"
            ) == "complete"
        )

    def by_test_id(self, test_id):
        return self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f'[data-testid="{test_id}"]')
            )
        )

    def safe_click(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

        self.wait.until(
            lambda driver: element.is_displayed() and element.is_enabled()
        )

        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

    def fill_valid_form(self, select_communication=True):
        Select(
            self.by_test_id("forms-country")
        ).select_by_visible_text(TEST_DATA["country"])

        Select(
            self.by_test_id("forms-title")
        ).select_by_visible_text(TEST_DATA["title"])

        self.by_test_id("forms-first-name").send_keys(
            TEST_DATA["first_name"]
        )
        self.by_test_id("forms-last-name").send_keys(
            TEST_DATA["last_name"]
        )

        self.driver.find_element(
            By.ID, "forms-dob"
        ).send_keys(TEST_DATA["dob"])

        self.by_test_id("forms-doj").send_keys(TEST_DATA["doj"])
        self.by_test_id("forms-email").send_keys(TEST_DATA["email"])

        Select(
            self.by_test_id("forms-phone-code")
        ).select_by_visible_text(TEST_DATA["phone_code"])

        self.by_test_id("forms-phone-number").send_keys(
            TEST_DATA["phone_number"]
        )

        if select_communication:
            self.safe_click(
                self.by_test_id("forms-comm-email")
            )

    def assert_text_visible(self, text):
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//*[normalize-space()='{text}']")
            )
        )

    # TC01: Valid form submission
    def test_TC01_valid_form_submission(self):
        self.fill_valid_form()
        self.safe_click(self.by_test_id("forms-submit"))

        success = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="forms-success"]')
            )
        )

        self.assertIn("Details Successfully Added", success.text)

    # TC02: Empty form validation
    def test_TC02_empty_form_validation(self):
        self.safe_click(self.by_test_id("forms-submit"))
        self.assert_text_visible("First Name is required")

    # TC03: Invalid email validation
    def test_TC03_invalid_email_validation(self):
        self.fill_valid_form()

        email = self.by_test_id("forms-email")
        email.clear()
        email.send_keys("notanemail")

        is_valid = self.driver.execute_script(
            "return arguments[0].validity.valid;",
            email
        )

        if not is_valid:
            self.assertFalse(is_valid)
        else:
            self.safe_click(self.by_test_id("forms-submit"))
            self.assert_text_visible("Invalid Email Address")

    # TC04: Invalid joining date format
    def test_TC04_invalid_joining_date_format(self):
        self.fill_valid_form()

        doj = self.by_test_id("forms-doj")
        doj.clear()
        doj.send_keys("2021-06-01")

        self.safe_click(self.by_test_id("forms-submit"))

        self.assert_text_visible(
            "Date of Joining format should be dd/mm/yyyy"
        )

    # TC05: Missing communication preference
    def test_TC05_missing_communication_preference(self):
        self.fill_valid_form(select_communication=False)
        self.safe_click(self.by_test_id("forms-submit"))

        self.assert_text_visible(
            "Please select a Communication Preference"
        )

    # TC06: Country dropdown options
    def test_TC06_country_dropdown_options(self):
        country = Select(self.by_test_id("forms-country"))
        options = [option.text.strip() for option in country.options]

        for expected in [
            "United States",
            "Canada",
            "United Kingdom",
            "India",
            "Australia",
            "Other"
        ]:
            self.assertIn(expected, options)

    # TC07: Clear resets form fields
    def test_TC07_clear_resets_form_fields(self):
        self.fill_valid_form()
        self.safe_click(self.by_test_id("forms-clear"))

        for field in [
            "forms-first-name",
            "forms-last-name",
            "forms-email",
            "forms-phone-number"
        ]:
            self.assertEqual(
                self.by_test_id(field).get_attribute("value"),
                ""
            )

        self.assertFalse(
            self.by_test_id("forms-comm-email").is_selected()
        )

    # TC08: Communication radio buttons are exclusive
    def test_TC08_communication_radio_buttons_are_exclusive(self):
        email = self.by_test_id("forms-comm-email")
        phone = self.by_test_id("forms-comm-phone")

        self.safe_click(email)
        self.assertTrue(email.is_selected())

        self.safe_click(phone)
        self.assertTrue(phone.is_selected())
        self.assertFalse(email.is_selected())


if __name__ == "__main__":
    unittest.main(verbosity=2)