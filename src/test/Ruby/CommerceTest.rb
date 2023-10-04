require 'selenium-webdriver'
require 'test/unit'

class CommerceTest < Test::Unit::TestCase
  def setup
    options = Selenium::WebDriver::Chrome::Options.new
    options.add_argument('--headless=new')
    @driver = Selenium::WebDriver.for :chrome, options: options
    @driver.manage.timeouts.implicit_wait = 4 # seconds
    @driver.manage.window.resize_to(1920, 1080)
    @wait = Selenium::WebDriver::Wait.new(timeout: 10) # seconds
  end

  def test_commerce
    username = 'standard_user'
    password = 'secret_sauce'

    @driver.navigate.to 'https://www.saucedemo.com'
    @driver.find_element(id: 'user-name').send_keys(username);
    @driver.find_element(id: 'password').send_keys(password);
    @driver.find_element(id: 'login-button').click

    @driver.find_element(id: 'add-to-cart-sauce-labs-backpack').click
    @driver.find_element(id: 'shopping_cart_container').click

    cart_page_element = @driver.find_element(class: 'cart_list')
    @wait.until { cart_page_element.displayed? }

    cart_item_name = @driver.find_element(class: 'inventory_item_name').text
    assert_equal(cart_item_name, 'Sauce Labs Backpack')

    @driver.find_element(id: 'checkout').click

    checkout_page_element = @driver.find_element(id: 'checkout_info_container')
    @wait.until { checkout_page_element.displayed? }

    @driver.find_element(id: 'first-name').send_keys('John')
    @driver.find_element(id: 'last-name').send_keys('Doe')
    @driver.find_element(id: 'postal-code').send_keys('10001')
    @driver.find_element(id: 'continue').click

    checkout_item_name = @driver.find_element(class: 'inventory_item_name').text
    assert_equal(checkout_item_name, 'Sauce Labs Backpack')

    @driver.find_element(id: 'finish').click

    success_is_displayed = @driver.find_element(id: 'checkout_complete_container').displayed?
    assert_true(success_is_displayed)
  end
end
