require 'selenium-webdriver'
require 'test/unit'

class CommerceTest < Test::Unit::TestCase
  USERNAME = 'standard_user'.freeze
  LOCKEDUSERNAME = 'locked_out_user'.freeze
  GLITCHUSERNAME = 'performance_glitch_user'.freeze
  PASSWORD = 'secret_sauce'.freeze

  def setup_driver(url)
    options = Selenium::WebDriver::Chrome::Options.new
    options.add_argument('--headless=new')
    @driver = Selenium::WebDriver.for :chrome, options: options
    @driver.manage.timeouts.implicit_wait = 4 # seconds
    @driver.manage.window.resize_to(1920, 1080)
    @wait = Selenium::WebDriver::Wait.new(timeout: 10) # seconds
    @driver.navigate.to url

    @actions = @driver.action
  end

  def log_in(username, password)
    @driver.find_element(id: 'user-name').send_keys(username)
    @driver.find_element(id: 'password').send_keys(password)
    @driver.find_element(id: 'login-button').click

    elements = @driver.find_elements(id: 'inventory_container')
    assert_true(elements.size > 0)
  end

  def log_out
    @driver.find_element(id: 'react-burger-menu-btn').click
    @driver.find_element(id: 'logout_sidebar_link').click

    elements = @driver.find_elements(class: 'login_container')
    assert_true(elements.size > 0)
  end

  def teardown
    log_out
    @driver.quit
  end

  def buy_backpack
    setup_driver('https://www.saucedemo.com')
    log_in(USERNAME, PASSWORD)

    # Click "Add to cart" for the backpack item
    @driver.find_element(id: 'add-to-cart-sauce-labs-backpack').click
    # Click on the cart icon
    @driver.find_element(id: 'shopping_cart_container').click

    # Explicit wait until the page is loaded.
    cart_page_element = @driver.find_element(class: 'cart_list')
    @wait.until { cart_page_element.displayed? }

    # Assert that the item name is correctly displayed on the
    # cart page.
    cart_item_name = @driver.find_element(class: 'inventory_item_name').text
    assert_equal(cart_item_name, 'Sauce Labs Backpack')

    # Click on the checkout button
    @driver.find_element(id: 'checkout').click

    # Wait until the checkout page is displayed
    checkout_page_element = @driver.find_element(id: 'checkout_info_container')
    @wait.until { checkout_page_element.displayed? }

    # Fill in the credentials
    @driver.find_element(id: 'first-name').send_keys('John')
    @driver.find_element(id: 'last-name').send_keys('Doe')
    @driver.find_element(id: 'postal-code').send_keys('10001')
    @driver.find_element(id: 'continue').click

    # Assert that the checkout item name is correct
    checkout_item_name = @driver.find_element(class: 'inventory_item_name').text
    assert_equal(checkout_item_name, 'Sauce Labs Backpack')

    # Click on the finish button
    @driver.find_element(id: 'finish').click

    # Assert that the success page is visible
    success_is_displayed = @driver.find_element(id: 'checkout_complete_container').displayed?
    assert_true(success_is_displayed)
  end

  def test_assert_item_name_on_item_info_page
    setup_driver('https://www.saucedemo.com')
    log_in(USERNAME, PASSWORD)

    # go to the item
    @driver.find_element(id: 'item_4_title_link').click

    # check that texts exist on the site
    assert_equal(@driver.find_element(class: 'inventory_details_name').text, "Sauce Labs Backpack")
    expected = "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection."
    assert_equal(@driver.find_element(class: 'inventory_details_desc').text, expected)

  end

  def test_move_to_linkedin
    setup_driver('https://www.saucedemo.com')
    log_in(USERNAME, PASSWORD)
  
    # Scroll down
    linkedin_element = @driver.find_element(class: 'social_linkedin')
    @actions.move_to(linkedin_element).perform
    # Go to Linkedin page
    linkedin_element.click
  
    # Verify you are on the Linkedin page
    tab_list = @driver.window_handles
    @driver.switch_to.window(tab_list[1])
  
    assert_equal('https://www.linkedin.com/company/sauce-labs/', @driver.current_url)
    @driver.close
    @driver.switch_to.window(tab_list[0])
  end
  
  def test_assert_sorting
    setup_driver('https://www.saucedemo.com')
    log_in(USERNAME, PASSWORD)
  
    # Click the filters box and select Z-A
    @driver.find_element(class: 'select_container').click
    @driver.find_element(css: "option[value='za']").click
    # Check that the name at the top is "Test.allTheThings() T-Shirt (Red)"
    assert_equal('Test.allTheThings() T-Shirt (Red)', @driver.find_element(css: '.inventory_item_name').text)
  
    # Click the filters box and select A-Z
    @driver.find_element(class: 'select_container').click
    @driver.find_element(css: "option[value='az']").click
    # Check that the name at the top is "Sauce Labs Backpack"
    assert_equal('Sauce Labs Backpack', @driver.find_element(css: '.inventory_item_name').text)
  
    # Click the filters box and select Low-High
    @driver.find_element(class: 'select_container').click
    @driver.find_element(css: "option[value='hilo']").click
    # Check that the name at the top is "Sauce Labs Onesie"
    assert_equal('Sauce Labs Fleece Jacket', @driver.find_element(css: '.inventory_item_name').text)
  
    # Click the filters box and select High-Low
    @driver.find_element(class: 'select_container').click
    @driver.find_element(css: "option[value='lohi']").click
    # Check that the name at the top is "Sauce Labs Fleece Jacket"
    assert_equal('Sauce Labs Onesie', @driver.find_element(css: '.inventory_item_name').text)
  end

  def test_assert_shopping_button_states
    setup_driver('https://www.saucedemo.com')
    log_in(USERNAME, PASSWORD)
  
    # Add items to cart
    @driver.find_elements(css: "[id^=add-to-cart]").each do |button|
      @actions.move_to(button).perform
      button.click
    end
  
    # Check that the cart button says 6
    assert_equal('6', @driver.find_element(class: 'shopping_cart_badge').text)
  
    # Remove items from cart
    @driver.find_elements(css: "[id^=remove]").each do |button|
      @actions.move_to(button).perform
      button.click
    end
  
    # Check that the cart button says nothing
    assert_true(@driver.find_elements(class: 'shopping_cart_badge').size < 1)
  end
  
  def test_assert_user_log_in_cache_permanency
    setup_driver('https://www.saucedemo.com')
    log_in(USERNAME, PASSWORD)
  
    # Add items to cart
    backpack_button = @driver.find_element(id: 'add-to-cart-sauce-labs-backpack')
    @actions.move_to(backpack_button).perform
    backpack_button.click
  
    bike_light_button = @driver.find_element(id: 'add-to-cart-sauce-labs-bike-light')
    @actions.move_to(bike_light_button).perform
    bike_light_button.click
  
    log_out
  
    # Check that items are still in the cart
    log_in(USERNAME, PASSWORD)
    assert_equal('2', @driver.find_element(class: 'shopping_cart_badge').text)
  end

  def test_assert_app_reset_functionality  # flaky test
    setup_driver('https://www.saucedemo.com')
    log_in(USERNAME, PASSWORD)
  
    # Select all items
    @driver.find_elements(css: "[id^=add-to-cart]").each do |button|
      @actions.move_to(button).perform
      button.click
    end
  
    # Click on sidebar
    @driver.find_element(id: 'react-burger-menu-btn').click
    # Click on Reset App State
    @driver.find_element(id: 'reset_sidebar_link').click
    # Click on the close sidebar button using JS.
    # This was necessary because normal click was not waiting 
    # for the CSS animation to be over, resulting in an
    # element click interception.
    @driver.execute_script("arguments[0].click();", @driver.find_element(id: 'react-burger-cross-btn'))
  
    # Check that the app reset but that there is a bug with "Remove" still staying instead of resetting to Add Cart
    assert_true(@driver.find_elements(class: 'shopping_cart_badge').size < 1)
  
    # Verify the visibility of 'remove' buttons
    assert_true(@driver.find_element(id: 'remove-sauce-labs-backpack').displayed?)
    assert_true(@driver.find_element(id: 'remove-sauce-labs-bike-light').displayed?)
    assert_true(@driver.find_element(id: 'remove-sauce-labs-bolt-t-shirt').displayed?)
    assert_true(@driver.find_element(id: 'remove-sauce-labs-fleece-jacket').displayed?)
    assert_true(@driver.find_element(id: 'remove-sauce-labs-onesie').displayed?)
    assert_true(@driver.find_element(id: 'remove-test.allthethings()-t-shirt-(red)').displayed?)
  end
  
  def test_assert_error_accessing_without_log_in
    setup_driver('https://www.saucedemo.com/cart.html')  # write the direct link here
  
    # Assert that the error is the correct one
    expected = 'Epic sadface: You can only access \'/cart.html\' when you are logged in.'
    assert_equal(expected, @driver.find_element(class: 'error-message-container').text)
  
    log_in(USERNAME, PASSWORD)
  
    # Now try logging in and then jumping to a link
    @driver.navigate.to('https://www.saucedemo.com/cart.html')
  
    # Assert that it worked when you were logged in
    assert_true(@driver.find_element(id: 'cart_contents_container').displayed?)
  end

  def test_assert_locked_out_user
    setup_driver('https://www.saucedemo.com')
    
    # Enter LOCKEDUSERNAME and PASSWORD and try to log in
    @driver.find_element(id: 'user-name').send_keys(LOCKEDUSERNAME)
    @driver.find_element(id: 'password').send_keys(PASSWORD)
    @driver.find_element(id: 'login-button').click
    
    # Clear the input fields
    @driver.find_element(id: 'user-name').send_keys(:control, 'a', :backspace)
    @driver.find_element(id: 'password').send_keys(:control, 'a', :backspace)
    
    # Assert the error
    expected = 'Epic sadface: Sorry, this user has been locked out.'
    assert_equal(expected, @driver.find_element(class: 'error-message-container').text)
    
    # Attempt to log in with the normal user
    log_in(USERNAME, PASSWORD)
  end

  def test_glitched_user_experience
    setup_driver('https://www.saucedemo.com')
    log_in(GLITCHUSERNAME, PASSWORD)

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
