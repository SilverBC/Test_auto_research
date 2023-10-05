const {Builder, By, until, Capabilities} = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const assert = require('assert');
const { describe, it, after } = require('mocha');

describe('CommerceTest', function() {
    let driver;

    before(async function () {
	const chromeOptions = new chrome.Options().addArguments("--headless=new");
	driver = await new Builder()
	      .forBrowser('chrome')
	      .setChromeOptions(chromeOptions)
	      .build();
	await driver.manage().setTimeouts({implicit: 4000});
	await driver.manage().window().setRect({width: 1920, height: 1080});
    });

    it('should run test', async function() {
	 const USERNAME = "standard_user";
	 const PASSWORD = "secret_sauce";

	 await driver.get('https://www.saucedemo.com');

	 await driver.findElement(By.id('user-name')).sendKeys(USERNAME);
	 await driver.findElement(By.id('password')).sendKeys(PASSWORD);
	 await driver.findElement(By.id('login-button')).click();

	 await driver.findElement(By.id('add-to-cart-sauce-labs-backpack')).click();
	 await driver.findElement(By.id('shopping_cart_container')).click();

	 const cartPageElement = await driver.findElement(By.className('cart_list'));
	 await driver.wait(until.elementIsVisible(cartPageElement), 10000);

	 const cartItemName = await driver.findElement(By.className('inventory_item_name')).getText();
	 assert.strictEqual(cartItemName, 'Sauce Labs Backpack');

	 await driver.findElement(By.id('checkout')).click();
	 const checkoutPageElement = await driver.findElement(By.id('checkout_info_container'));
	 await driver.wait(until.elementIsVisible(checkoutPageElement), 10000);

	 await driver.findElement(By.id('first-name')).sendKeys('John');
	 await driver.findElement(By.id('last-name')).sendKeys('Doe');
	 await driver.findElement(By.id('postal-code')).sendKeys('10001');
	 await driver.findElement(By.id('continue')).click();

	 const checkoutItemName = await driver.findElement(By.className('inventory_item_name')).getText();
	 assert.strictEqual(checkoutItemName, 'Sauce Labs Backpack');

	 await driver.findElement(By.id('finish')).click();

	 const successIsDisplayed = await driver.findElement(By.id('checkout_complete_container')).isDisplayed();
	 assert(successIsDisplayed);

    });

    after(async function() {
	await driver.quit();
    });
});
