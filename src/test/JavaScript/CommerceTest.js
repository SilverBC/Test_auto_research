const {Builder, By, until, Capabilities, Key, ActionSequence} = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const assert = require('assert');
const { describe, it, after } = require('mocha');

describe('CommerceTest', function() {
    this.timeout(15000);

    const USERNAME = "standard_user";
    const LOCKEDUSERNAME = "locked_out_user";
    const GLITCHUSERNAME = "performance_glitch_user";
    const PASSWORD = "secret_sauce";
    
    let driver;
    let wait;
    let actions;

    async function setUp(url) {
        const chromeOptions = new chrome.Options().addArguments('--headless=new');
        driver = await new Builder()
            .forBrowser('chrome')
            .setChromeOptions(chromeOptions)
            .build();
        await driver.manage().setTimeouts({implicit: 4000});
        await driver.manage().window().setRect({width: 1920, height: 1080});
        wait = driver.wait;
        actions = driver.actions();
        await driver.get(url);
    }

    async function logIn(name, password) {
        await driver.findElement(By.id('user-name')).sendKeys(name);
        await driver.findElement(By.id('password')).sendKeys(password);
        await driver.findElement(By.id('login-button')).click();

	// Assert that the store page became visible
        assert(await driver.findElement(By.id('inventory_container')).isDisplayed());
    }

    async function logOut() {
        await driver.findElement(By.id('react-burger-menu-btn')).click();
        await driver.findElement(By.id('logout_sidebar_link')).click();

	// Assert that the login page is visible
        assert(await driver.findElement(By.className('login_container')).isDisplayed());
    }

    afterEach(async function() {
	await logOut();
        await driver.quit();
    })

    it('buy backpack', async function() {
        await setUp('https://www.saucedemo.com');
        await logIn(USERNAME, PASSWORD);

	// Click "Add to cart" for the backpack item
        await driver.findElement(By.id('add-to-cart-sauce-labs-backpack')).click();
	// Click on the cart icon
        await driver.findElement(By.id('shopping_cart_container')).click();

	// Explicit wait until the page is loaded.
        const cartPageElement = await driver.findElement(By.className('cart_list'));
        await wait(until.elementIsVisible(cartPageElement), 10000);

	// Assert that the item name is correctly displayed on the
	// cart page.
        const cartItemName = await driver.findElement(By.className('inventory_item_name')).getText();
        assert.strictEqual(cartItemName, 'Sauce Labs Backpack');

	// Click on the checkout button
        await driver.findElement(By.id('checkout')).click();

	// Wait until the checkout page is displayed
        const checkoutPageElement = await driver.findElement(By.id('checkout_info_container'));
        await wait(until.elementIsVisible(checkoutPageElement), 10000);

	// Fill in the credentials
        await driver.findElement(By.id('first-name')).sendKeys('John');
        await driver.findElement(By.id('last-name')).sendKeys('Doe');
        await driver.findElement(By.id('postal-code')).sendKeys('10001');
        await driver.findElement(By.id('continue')).click();

	// Assert that the checkout item name is correct
        const checkoutItemName = await driver.findElement(By.className('inventory_item_name')).getText();
        assert.strictEqual(checkoutItemName, 'Sauce Labs Backpack');

	// Click on the finish button
        await driver.findElement(By.id('finish')).click();

	// Assert that the success page is visible
        const successIsDisplayed = await driver.findElement(By.id('checkout_complete_container')).isDisplayed();
        assert(successIsDisplayed);
    });

    it('assert item name on item info page', async function() {
	await setUp('https://www.saucedemo.com');
	await logIn(USERNAME, PASSWORD);
	
        //go to the item
	await driver.findElement(By.id('item_4_title_link')).click();
	
        //Check that texts exist on the site 
        // Sauce Labs Backpack

	assert.strictEqual(await driver.findElement(By.className('inventory_details_name')).getText(), 'Sauce Labs Backpack');
	
	const expectedDesc = "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.";
	assert.strictEqual(await driver.findElement(By.className('inventory_details_desc')).getText(), expectedDesc);
    });
    
    it('Move To LinkedIn', async function() {
	await setUp('https://www.saucedemo.com');
	await logIn(USERNAME, PASSWORD);
	
        //Scroll down
	const linkedInElement = await driver.findElement(By.className('social_linkedin'));
	await driver.actions().move({origin: linkedInElement}).click().perform();	

        //Go to Linkedin page
	const handles = await driver.getAllWindowHandles();
	await driver.switchTo().window(handles[1]);
	
        //Verify you are on the Linkedin page
	const currentURL = await driver.getCurrentUrl();
	assert(currentURL.startsWith('https://www.linkedin.com/company/sauce-labs/'));
	
	await driver.close();
	await driver.switchTo().window(handles[0]);
    });

    it('Assert Sorting', async function() {
	await setUp('https://www.saucedemo.com');
	await logIn(USERNAME, PASSWORD);
	
	// Click the filters box
	await driver.findElement(By.className("select_container")).click();
	// Click Z-A
	await driver.findElement(By.css("option[value='za']")).click();
	// Check that the name at the top is "Test.allTheThings() T-Shirt (Red)"
	let itemName = await driver.findElement(By.css(".inventory_item_name")).getText();
	assert.strictEqual(itemName, "Test.allTheThings() T-Shirt (Red)");
	
	// Click the filters box
	await driver.findElement(By.className("select_container")).click();
	// Click A-Z 
	await driver.findElement(By.css("option[value='az']")).click();
	// Check that the name at the top is "Sauce Labs Backpack"
	itemName = await driver.findElement(By.css(".inventory_item_name")).getText();
	assert.strictEqual(itemName, "Sauce Labs Backpack");
	
	// Click the filters box
	await driver.findElement(By.className("select_container")).click();
	// Click low-High
	await driver.findElement(By.css("option[value='hilo']")).click();
	// Check that the name at the top is "Sauce Labs Onesie"
	itemName = await driver.findElement(By.css(".inventory_item_name")).getText();
	assert.strictEqual(itemName, "Sauce Labs Fleece Jacket");
	
	// Click the filters box
	await driver.findElement(By.className("select_container")).click();
	// Click high-Low
	await driver.findElement(By.css("option[value='lohi']")).click();
	// Check that the name at the top is "Sauce Labs Fleece Jacket"
	itemName = await driver.findElement(By.css(".inventory_item_name")).getText();
	assert.strictEqual(itemName, "Sauce Labs Onesie");
    });
    
    it('Assert Shopping Button States', async function() {
	await setUp('https://www.saucedemo.com');
	await logIn(USERNAME, PASSWORD);
	
	let buttonsToAdd = await driver.findElements(By.css("[id^=add-to-cart]"));
	for(let button of buttonsToAdd) {
	    await driver.actions().move({origin: button}).perform();
	    await button.click();
	}
	
	// Check that the cart button says 6
	let cartCount = await driver.findElement(By.className("shopping_cart_badge")).getText();
	assert.strictEqual(cartCount, "6");
	
	let buttonsToRemove = await driver.findElements(By.css("[id^=remove]"));
	for(let button of buttonsToRemove) {
	    await driver.actions().move({origin: button}).perform();
	    await button.click();
	}
	
	// Check that the cart button says nothing
	let cartBadges = await driver.findElements(By.className("shopping_cart_badge"));
	assert(cartBadges.length < 1);
    });
    
    it('Assert User Log In Cache Permanency', async function() { 
        await setUp('https://www.saucedemo.com');
        await logIn(USERNAME, PASSWORD);

        //Add items to cart
        const backpackButton = await driver.findElement(By.id('add-to-cart-sauce-labs-backpack'));
        await driver.actions().move({origin: backpackButton}).perform();
        await backpackButton.click();

        const bikeLightButton = await driver.findElement(By.id('add-to-cart-sauce-labs-bike-light'));
        await driver.actions().move({origin: bikeLightButton}).perform();
        await bikeLightButton.click();

        await logOut();

        //check that items are still in the cart
        await logIn(USERNAME, PASSWORD);
        const cartBadgeText = await driver.findElement(By.className('shopping_cart_badge')).getText();
        assert.strictEqual(cartBadgeText, '2');
    });

    it('Assert App Reset Functionality', async function() {   //flaky test
        await setUp('https://www.saucedemo.com');
        await logIn(USERNAME, PASSWORD);

        //select all items
        const addButtons = await driver.findElements(By.css("[id^=add-to-cart]"));
        for(let button of addButtons) {
            await driver.actions().move({origin: button}).perform();
            await button.click();
        }

        //click on sidebar
        await driver.findElement(By.id('react-burger-menu-btn')).click();
        //click on Reset App State
        await driver.findElement(By.id('reset_sidebar_link')).click();
        // Click on the close sidebar button using JS.
        // This was necessary because normal click was not waiting 
        // for the CSS animation to be over, resulting in an
        // element click interception.
        await driver.executeScript("arguments[0].click()", driver.findElement(By.id('react-burger-cross-btn')));

        //check that the app reset but that there is a bug with "Remove" still staying instead of resetting to Add Cart
        const cartBadges = await driver.findElements(By.className('shopping_cart_badge'));
        assert(cartBadges.length < 1);

        assert(await driver.findElement(By.id('remove-sauce-labs-backpack')).isDisplayed());
        assert(await driver.findElement(By.id('remove-sauce-labs-bike-light')).isDisplayed());
        assert(await driver.findElement(By.id('remove-sauce-labs-bolt-t-shirt')).isDisplayed());
        assert(await driver.findElement(By.id('remove-sauce-labs-fleece-jacket')).isDisplayed());
        assert(await driver.findElement(By.id('remove-sauce-labs-onesie')).isDisplayed());
        assert(await driver.findElement(By.id('remove-test.allthethings()-t-shirt-(red)')).isDisplayed());
    });

    it('Assert Error Accessing Without Log In', async function() {
        await setUp('https://www.saucedemo.com/cart.html');  // Direct link

        //assert that the error is the correct one
        const errorMessage = await driver.findElement(By.className('error-message-container')).getText();
        const expectedMessage = "Epic sadface: You can only access '/cart.html' when you are logged in.";
        assert.strictEqual(errorMessage, expectedMessage);

        await logIn(USERNAME, PASSWORD);

        //now try logging in and then jumping to a link
        await driver.get('https://www.saucedemo.com/cart.html');

        //assert that it worked when you were logged in
        const cartContainerDisplayed = await driver.findElement(By.id('cart_contents_container')).isDisplayed();
        assert(cartContainerDisplayed);
    });

    it('Assert Locked Out User', async function() {
        await setUp('https://www.saucedemo.com');

        await driver.findElement(By.id('user-name')).sendKeys(LOCKEDUSERNAME);
        await driver.findElement(By.id('password')).sendKeys(PASSWORD);
        await driver.findElement(By.id('login-button')).click();

        await driver.findElement(By.id('user-name')).sendKeys(Key.CONTROL + "a", Key.BACK_SPACE);
        await driver.findElement(By.id('password')).sendKeys(Key.CONTROL + "a", Key.BACK_SPACE);

        //assert the error
        const errorMessage = await driver.findElement(By.className('error-message-container')).getText();
        const expectedMessage = "Epic sadface: Sorry, this user has been locked out.";
        assert.strictEqual(errorMessage, expectedMessage);

        //attempt to get in with the normal user
        await logIn(USERNAME, PASSWORD);
    });

    it('Glitched User Experience', async function() {
        await setUp('https://www.saucedemo.com');
        await logIn(GLITCHUSERNAME, PASSWORD);

        //jump in with the Glitched user 
        await driver.findElement(By.id('add-to-cart-sauce-labs-backpack')).click();
        await driver.findElement(By.id('shopping_cart_container')).click();

        const cartPageElement = await driver.findElement(By.className('cart_list'));
        await wait(until.elementIsVisible(cartPageElement), 10000);

        const cartItemName = await driver.findElement(By.className('inventory_item_name')).getText();
        assert.strictEqual(cartItemName, 'Sauce Labs Backpack');

        await driver.findElement(By.id('checkout')).click();
        const checkoutPageElement = await driver.findElement(By.id('checkout_info_container'));
        await wait(until.elementIsVisible(checkoutPageElement), 10000);

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

});
