import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CommerceTest(unittest.TestCase):

    def test_commerce(self):
        USERNAME = "standard_user"
        PASSWORD = "secret_sauce"

        options = webdriver.ChromeOptions()
        # options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(4)  # seconds
        driver.set_window_size(1920, 1080)
        wait = WebDriverWait(driver, 10)  # seconds

        driver.get("https://www.saucedemo.com")

        driver.find_element(By.ID, "user-name").send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "login-button").click()

        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        driver.find_element(By.ID, "shopping_cart_container").click()

        cart_page_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cart_list")))
        cart_item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        self.assertEqual(cart_item_name, "Sauce Labs Backpack")

        driver.find_element(By.ID, "checkout").click()
        checkout_page_element = wait.until(EC.visibility_of_element_located((By.ID, "checkout_info_container")))

        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("10001")
        driver.find_element(By.ID, "continue").click()

        checkout_item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        self.assertEqual(checkout_item_name, "Sauce Labs Backpack")

        driver.find_element(By.ID, "finish").click()
        success_is_displayed = driver.find_element(By.ID, "checkout_complete_container").is_displayed()
        self.assertTrue(success_is_displayed)

if __name__ == "__main__":
    unittest.main()
