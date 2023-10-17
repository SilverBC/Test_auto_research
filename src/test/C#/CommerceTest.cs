using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;
using Xunit;
using System;
using System.Collections.Generic;
using OpenQA.Selenium.Interactions;
using System.Linq;
using System.Threading;

public class CommerceTest
{
    private const string USERNAME = "standard_user";
    private const string LOCKEDUSERNAME = "locked_out_user";
    private const string GLITCHUSERNAME = "performance_glitch_user";
    private const string PASSWORD = "secret_sauce";

    private IWebDriver driver;
    private WebDriverWait wait;
    private Actions actions;

    public void SetUp(string url)
    {
        ChromeOptions options = new ChromeOptions();
        options.AddArguments("--headless=new"); // Uncomment if you want to run headless
        driver = new ChromeDriver(options);
        driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(4);
        driver.Manage().Window.Size = new System.Drawing.Size(1920, 1080);
        wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
        driver.Navigate().GoToUrl(url);

        actions = new Actions(driver);
    }

    public void LogIn(string name, string password)
    {
        driver.FindElement(By.Id("user-name")).SendKeys(name);
        driver.FindElement(By.Id("password")).SendKeys(password);
        driver.FindElement(By.Id("login-button")).Click();

        IReadOnlyCollection<IWebElement> elements = driver.FindElements(By.Id("inventory_container"));
        Assert.True(elements.Count > 0);
    }

    public void LogOut()
    {
        driver.FindElement(By.Id("react-burger-menu-btn")).Click();
        driver.FindElement(By.Id("logout_sidebar_link")).Click();

        IReadOnlyCollection<IWebElement> elements = driver.FindElements(By.ClassName("login_container"));
        Assert.True(elements.Count > 0);
    }

    public void Teardown()
    {
        LogOut();
        driver.Quit();
    }


    // FIXME: Public method 'SetUp' on test class 'CommerceTest' should be marked as a Theory. (https://xunit.github.io/xunit.analyzers/rules/xUnit1013)


    // TODO: Change all invocations of teardown to Aftertest or smth.

    [Fact]
    public void BuyBackpack()
    {
        SetUp("https://www.saucedemo.com");
        LogIn(USERNAME, PASSWORD);

	// Click "Add to cart" for the backpack item
        driver.FindElement(By.Id("add-to-cart-sauce-labs-backpack")).Click();

	// Click on the cart icon
        driver.FindElement(By.Id("shopping_cart_container")).Click();

	// Explicit wait until the page is loaded.
        IWebElement cartPageElement = driver.FindElement(By.ClassName("cart_list"));
        wait.Until(d => cartPageElement.Displayed);

	// Assert that the item name is correctly displayed on the
	// cart page.
        string cartItemName = driver.FindElement(By.ClassName("inventory_item_name")).Text;
        Assert.Equal("Sauce Labs Backpack", cartItemName);

	// Click on the checkout button
        driver.FindElement(By.Id("checkout")).Click();

	// Wait until the checkout page is displayed
        IWebElement checkoutPageElement = driver.FindElement(By.Id("checkout_info_container"));
        wait.Until(d => checkoutPageElement.Displayed);

	// Fill in the credentials
        driver.FindElement(By.Id("first-name")).SendKeys("John");
        driver.FindElement(By.Id("last-name")).SendKeys("Doe");
        driver.FindElement(By.Id("postal-code")).SendKeys("10001");
        driver.FindElement(By.Id("continue")).Click();

	// Assert that the checkout item name is correct
        string checkoutItemName = driver.FindElement(By.ClassName("inventory_item_name")).Text;
        Assert.Equal("Sauce Labs Backpack", checkoutItemName);

	// Click on the finish button
        driver.FindElement(By.Id("finish")).Click();

	// Assert that the success page is visible
        bool successIsDisplayed = driver.FindElement(By.Id("checkout_complete_container")).Displayed;
        Assert.True(successIsDisplayed);

        Teardown();
    }

    [Fact]
    public void AssertItemNameOnItemInfoPage()
    {
        SetUp("https://www.saucedemo.com");
        LogIn(USERNAME, PASSWORD);

        // go to the item
        driver.FindElement(By.Id("item_4_title_link")).Click();

        // Check that texts exist on the site 
        // Sauce Labs Backpack
        Assert.Equal("Sauce Labs Backpack", driver.FindElement(By.ClassName("inventory_details_name")).Text);
        string expected = "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.";
        Assert.Equal(expected, driver.FindElement(By.ClassName("inventory_details_desc")).Text);
    
        Teardown();
    }

    [Fact]
    public void MoveToLinkedIn()
    {
        SetUp("https://www.saucedemo.com");
        LogIn(USERNAME, PASSWORD);

        // Scroll down
        actions.MoveToElement(driver.FindElement(By.ClassName("social_linkedin"))).Perform();

        // Go to Linkedin page
        driver.FindElement(By.ClassName("social_linkedin")).Click();

        // Verify you are on the Linkedin page
        var tabList = new List<string>(driver.WindowHandles);
        driver.SwitchTo().Window(tabList[1]);

        Assert.Equal("https://www.linkedin.com/company/sauce-labs/", driver.Url);
        driver.Close();
        driver.SwitchTo().Window(tabList[0]);
    
        Teardown();
    }

    [Fact]
    public void AssertSorting()
    {
        SetUp("https://www.saucedemo.com");
        LogIn(USERNAME, PASSWORD);

        // Click the filters box
        driver.FindElement(By.ClassName("select_container")).Click();
        // Click Z-A
        driver.FindElement(By.CssSelector("option[value='za']")).Click();
        // Check that the name at the top is "Test.allTheThings() T-Shirt (Red)
        Assert.Equal("Test.allTheThings() T-Shirt (Red)", driver.FindElement(By.CssSelector(".inventory_item_name")).Text);

        // Click the filters box
        driver.FindElement(By.ClassName("select_container")).Click();
        // Click A-Z
        driver.FindElement(By.CssSelector("option[value='az']")).Click();
        // Check that the name at the top is "Sauce Labs Backpack"
        Assert.Equal("Sauce Labs Backpack", driver.FindElement(By.CssSelector(".inventory_item_name")).Text);

        // Click the filters box
        driver.FindElement(By.ClassName("select_container")).Click();
        // Click low-High
        driver.FindElement(By.CssSelector("option[value='hilo']")).Click();
        // Check that the name at the top is "Sauce Labs Fleece Jacket"
        Assert.Equal("Sauce Labs Fleece Jacket", driver.FindElement(By.CssSelector(".inventory_item_name")).Text);

        // Click the filters box
        driver.FindElement(By.ClassName("select_container")).Click();
        // Click high-Low
        driver.FindElement(By.CssSelector("option[value='lohi']")).Click();
        // Check that the name at the top is "Sauce Labs Onesie"
        Assert.Equal("Sauce Labs Onesie", driver.FindElement(By.CssSelector(".inventory_item_name")).Text);
    
        Teardown();
    }

    [Fact]
    public void AssertShoppingButtonStates()
    {
        SetUp("https://www.saucedemo.com");
        LogIn(USERNAME, PASSWORD);

        IReadOnlyCollection<IWebElement> addToCartButtons = driver.FindElements(By.CssSelector("[id^=add-to-cart]"));
        
        foreach (IWebElement button in addToCartButtons)
        {
            new Actions(driver).MoveToElement(button).Perform();
            button.Click();
        };

        // Check that the cart button says 6
        Assert.Equal("6", driver.FindElement(By.ClassName("shopping_cart_badge")).Text);

        IReadOnlyCollection<IWebElement> removeButtons = driver.FindElements(By.CssSelector("[id^=remove]"));

        foreach (IWebElement button in removeButtons)
        {
            new Actions(driver).MoveToElement(button).Perform();
            button.Click();
        };

        // Check that the cart button says nothing
        Assert.True(driver.FindElements(By.ClassName("shopping_cart_badge")).Count < 1);
    
        Teardown();
    }

    [Fact]
    public void AssertUserLogInCachePermanency()
    {
        SetUp("https://www.saucedemo.com");
        LogIn(USERNAME, PASSWORD);

        // Add items to cart
        var backpackButton = driver.FindElement(By.Id("add-to-cart-sauce-labs-backpack"));
        new Actions(driver).MoveToElement(backpackButton).Perform();
        backpackButton.Click();

        var bikeLightButton = driver.FindElement(By.Id("add-to-cart-sauce-labs-bike-light"));
        new Actions(driver).MoveToElement(bikeLightButton).Perform();        //stale element error
        bikeLightButton.Click();

        LogOut();

        // Check that items are still in the cart
        LogIn(USERNAME, PASSWORD);

        Assert.Equal("2", driver.FindElement(By.ClassName("shopping_cart_badge")).Text);

        Teardown();
    }
    
    [Fact]
    public void AssertAppResetFunctionality()
    {
        SetUp("https://www.saucedemo.com");
        LogIn(USERNAME, PASSWORD);

        // Select all items
        IReadOnlyCollection<IWebElement> addToCartButtons = driver.FindElements(By.CssSelector("[id^=add-to-cart]"));
        
        foreach (IWebElement button in addToCartButtons)
        {
            new Actions(driver).MoveToElement(button).Perform();
            button.Click();
        };

        // Click on sidebar
        driver.FindElement(By.Id("react-burger-menu-btn")).Click();

        // Click on Reset App State
        driver.FindElement(By.Id("reset_sidebar_link")).Click();
        // Click on the close sidebar button using JS.
        // This was necessary because normal click was not waiting 
        // for the CSS animation to be over, resulting in an
        // element click interception.
        ((IJavaScriptExecutor)driver).ExecuteScript("arguments[0].click();", driver.FindElement(By.Id("react-burger-cross-btn")));

        // Check that the app reset but that there is a bug with "Remove" still staying instead of resetting to Add Cart
        Assert.True(driver.FindElements(By.ClassName("shopping_cart_badge")).Count < 1);

        // Check that "Remove" is displayed for each item
        Assert.True(driver.FindElement(By.Id("remove-sauce-labs-backpack")).Displayed);
        Assert.True(driver.FindElement(By.Id("remove-sauce-labs-bike-light")).Displayed);
        Assert.True(driver.FindElement(By.Id("remove-sauce-labs-bolt-t-shirt")).Displayed);
        Assert.True(driver.FindElement(By.Id("remove-sauce-labs-fleece-jacket")).Displayed);
        Assert.True(driver.FindElement(By.Id("remove-sauce-labs-onesie")).Displayed);
        Assert.True(driver.FindElement(By.Id("remove-test.allthethings()-t-shirt-(red)")).Displayed);

        Teardown();
    }

    [Fact]
    public void AssertErrorAccessingWithoutLogIn()
    {
        SetUp("https://www.saucedemo.com/cart.html");

        // Assert that the error is the correct one
        string expected = "Epic sadface: You can only access '/cart.html' when you are logged in.";
        Assert.Equal(expected, driver.FindElement(By.ClassName("error-message-container")).Text);

        LogIn(USERNAME, PASSWORD);

        // Now try logging in and then jumping to a link
        driver.Navigate().GoToUrl("https://www.saucedemo.com/cart.html");

        // Assert that it worked when you were logged in
        Assert.True(driver.FindElement(By.Id("cart_contents_container")).Displayed);

        Teardown();
    }

    [Fact]
    public void AssertLockedOutUser()
    {
        SetUp("https://www.saucedemo.com");
        driver.FindElement(By.Id("user-name")).SendKeys(LOCKEDUSERNAME);
        driver.FindElement(By.Id("password")).SendKeys(PASSWORD);
        driver.FindElement(By.Id("login-button")).Click();

        // Clear input fields for username and password
        driver.FindElement(By.Id("user-name")).SendKeys(Keys.Control + "a" + Keys.Backspace);
        driver.FindElement(By.Id("password")).SendKeys(Keys.Control + "a" + Keys.Backspace);

        // Assert the error
        string expected = "Epic sadface: Sorry, this user has been locked out.";
        Assert.Equal(expected, driver.FindElement(By.ClassName("error-message-container")).Text);

        // Attempt to get in with the normal user
        LogIn(USERNAME, PASSWORD);

        Teardown();
    }

    [Fact]
    public void Glitched_User_Experience()
    {
        SetUp("https://www.saucedemo.com");
        LogIn(GLITCHUSERNAME, PASSWORD);

        driver.FindElement(By.Id("add-to-cart-sauce-labs-backpack")).Click();
        driver.FindElement(By.Id("shopping_cart_container")).Click();

        IWebElement cartPageElement = driver.FindElement(By.ClassName("cart_list"));
        wait.Until(d => cartPageElement.Displayed);

        string cartItemName = driver.FindElement(By.ClassName("inventory_item_name")).Text;
        Assert.Equal("Sauce Labs Backpack", cartItemName);

        driver.FindElement(By.Id("checkout")).Click();
        IWebElement checkoutPageElement = driver.FindElement(By.Id("checkout_info_container"));
        wait.Until(d => checkoutPageElement.Displayed);

        driver.FindElement(By.Id("first-name")).SendKeys("John");
        driver.FindElement(By.Id("last-name")).SendKeys("Doe");
        driver.FindElement(By.Id("postal-code")).SendKeys("10001");
        driver.FindElement(By.Id("continue")).Click();

        string checkoutItemName = driver.FindElement(By.ClassName("inventory_item_name")).Text;
        Assert.Equal("Sauce Labs Backpack", checkoutItemName);

        driver.FindElement(By.Id("finish")).Click();

        bool successIsDisplayed = driver.FindElement(By.Id("checkout_complete_container")).Displayed;
        Assert.True(successIsDisplayed);

        Teardown();
    }

}
