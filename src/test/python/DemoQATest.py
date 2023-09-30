import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DemoQATest(unittest.TestCase):
    def scroll_past_element(self, driver, element):
        _ = element.location_once_scrolled_into_view
        ActionChains(driver).move_to_element(element).perform()

    def test_demoqa(self):
        USERNAME = "research_paper"
        PASSWORD = "1tq52rw43E!"

        dimension = (1920, 1080)
        options = Options()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(4)  # seconds
        driver.set_window_size(*dimension)
        wait = WebDriverWait(driver, 10)  # seconds

        # Load the login page
        driver.get("https://demoqa.com/login")

        # Input username and password, click login button
        driver.find_element(By.ID, "userName").send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "login").click()

        # Click "Go to Store" button
        store_button = driver.find_element(By.ID, "gotoStore")
        self.scroll_past_element(driver, store_button)
        store_button.click()

        # Click on the first book title
        driver.find_element(By.ID, "see-book-Git Pocket Guide").click()

        # Store the name of the book
        book_name = driver.find_element(By.CSS_SELECTOR, "#title-wrapper #userName-value").text

        # Add the book to the collection
        add_new_record_button = driver.find_element(By.ID, "addNewRecordButton")
        add_new_record_button.click()

        # Click profile button
        profile_button = driver.find_element(By.CSS_SELECTOR, ".show #item-3")
        self.scroll_past_element(driver, profile_button)
        profile_button.click()

        # Wait until the profile page is loaded. This takes a while.
        profile_element = driver.find_element(By.ID, "books-wrapper")
        wait.until(EC.visibility_of(profile_element))

        # Click on the first book in the profile table
        driver.find_element(By.ID, "see-book-Git Pocket Guide").click()

        # Get the book title and compare it to the stored value
        first_row_title_text = driver.find_element(By.CSS_SELECTOR, "#title-wrapper #userName-value").text
        self.assertEqual(first_row_title_text, book_name)

        # Go back to the profile page and delete the book.
        driver.back()
        driver.find_element(By.ID, "delete-record-undefined").click()

        driver.close()


if __name__ == "__main__":
    unittest.main()
