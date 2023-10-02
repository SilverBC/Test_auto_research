require 'selenium-webdriver'
require 'test/unit'

# IN THE MIDDLE OF DEBUGGING 


class DemoQATest < Test::Unit::TestCase
  def setup
    options = Selenium::WebDriver::Chrome::Options.new
    # options.add_argument('--headless=new')
    @driver = Selenium::WebDriver.for :chrome, options: options
    @driver.manage.timeouts.implicit_wait = 4 # seconds
    @driver.manage.window.resize_to(1920, 1080)
    @wait = Selenium::WebDriver::Wait.new(timeout: 10) # seconds
  end

  def scroll_past_element(element)
    @driver.switch_to.active_element.send_keys(:page_down)
  end

  def test_demoqa
    username = 'research_paper'
    password = '1tq52rw43E!'

    @driver.navigate.to 'https://demoqa.com/login'
    @driver.find_element(id: 'userName').send_keys(username)
    @driver.find_element(id: 'password').send_keys(password)
    @driver.find_element(id: 'login').click

    store_button = @driver.find_element(id: 'gotoStore')
    scroll_past_element(store_button)
    store_button = @driver.find_element(id: 'gotoStore')
    store_button.click

    @driver.find_element(xpath: "//*[@id='see-book-Git Pocket Guide']").click  # id is supposed to be used here instead of xpath
    book_name = @driver.find_element(xpath: '//*[@id="title-wrapper"]//*[@id="userName-value"]').text # css #title_wrapper #userName-value is supposed to be here
    add_new_record_button = @driver.find_element(id: 'addNewRecordButton')
    add_new_record_button.click

    profile_button = @driver.find_element(css: '.show #item-3')
    scroll_past_element(profile_button)
    profile_button.click

    profile_element = @driver.find_element(id: 'books-wrapper')
    @wait.until { profile_element.displayed? }

    @driver.find_element(id: 'see-book-Git Pocket Guide').click
    first_row_title_text = @driver.find_element(css: '#title-wrapper #userName-value').text
    assert_equal(book_name, first_row_title_text)

    @driver.navigate.back
    @driver.find_element(id: 'delete-record-undefined').click
  end

  def teardown
    @driver.quit
  end
end
