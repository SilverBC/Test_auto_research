const { Builder, By, until, Capabilities } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const assert = require('assert');
const { describe, it, after } = require('mocha');

describe('DemoQATest', function() {
    this.timeout(30000);
    let driver;
    
    before(async function() {
        const chromeOptions = new chrome.Options().addArguments('--headless=new');
        driver = await new Builder()
            .forBrowser('chrome')
            .setChromeOptions(chromeOptions)
            .build();
        await driver.manage().setTimeouts({ implicit: 4000 });
        await driver.manage().window().setRect({ width: 1920, height: 1080 });
    });
    
    it('should run test', async function() {
        const USERNAME = 'research_paper';
        const PASSWORD = '1tq52rw43E!';
        
        // Load the login page
        await driver.get('https://demoqa.com/login');
        
        // Input username and password, click login button
        await driver.findElement(By.id('userName')).sendKeys(USERNAME);
        await driver.findElement(By.id('password')).sendKeys(PASSWORD);
        await driver.findElement(By.id('login')).click();
        
        // Click "Go to Store" button
        const storeButton = await driver.findElement(By.id('gotoStore'));
        await driver.executeScript('arguments[0].scrollIntoView(); window.scrollBy(0, 200);', storeButton);
        await storeButton.click();
        
        // Click on the first book title
        await driver.findElement(By.id('see-book-Git Pocket Guide')).click();
        
        // Store the name of the book
        const bookName = await driver.findElement(By.css('#title-wrapper #userName-value')).getText();
        
        // Add the book to the collection
        const addNewRecordButton = await driver.findElement(By.id('addNewRecordButton'));
        await addNewRecordButton.click();
        
        // Click profile button
        const profileButton = await driver.findElement(By.css('.show #item-3'));
        await driver.executeScript('arguments[0].scrollIntoView(); window.scrollBy(0, 200);', profileButton);
        await profileButton.click();
        
        // Wait until the profile page is loaded. This takes a while.
        const profileElement = await driver.findElement(By.id('books-wrapper'));
        await driver.wait(until.elementIsVisible(profileElement), 10000);
        
        // Click on the first book in the profile table
        await driver.findElement(By.id('see-book-Git Pocket Guide')).click();
        
        // Get the book title and compare it to the stored value
        const firstRowTitleText = await driver.findElement(By.css('#title-wrapper #userName-value')).getText();
        assert.strictEqual(firstRowTitleText, bookName);
        
        // Go back to the profile page and delete the book.
        await driver.navigate().back();
        await driver.findElement(By.id('delete-record-undefined')).click();
    });
    
    after(async function() {
        await driver.quit();
    });
});
