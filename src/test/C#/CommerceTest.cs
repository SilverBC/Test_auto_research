using System;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;
using Xunit;

public class CommerceTest
{
    [Fact]
    public void Test()
    {
        string USERNAME = "standard_user";
        string PASSWORD = "secret_sauce";

        ChromeOptions options = new ChromeOptions();
        options.AddArguments("--headless");
        IWebDriver driver = new ChromeDriver(options);
        driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(4);
        driver.Manage().Window.Size = new System.Drawing.Size(1920, 1080);

        WebDriverWait wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));

        driver.Navigate().GoToUrl("https://www.saucedemo.com");

        driver.FindElement(By.Id("user-name")).SendKeys(USERNAME);
        driver.FindElement(By.Id("password")).SendKeys(PASSWORD);
        driver.FindElement(By.Id("login-button")).Click();

        driver.FindElement(By.Id("add-to-cart-sauce-labs-backpack")).Click();
        driver.FindElement(By.Id("shopping_cart_container")).Click();

        IWebElement cartPageElement = driver.FindElement(By.ClassName("cart_list"));
        wait.Until(SeleniumExtras.WaitHelpers.ExpectedConditions.ElementIsVisible(By.ClassName("cart_list")));

        string cartItemName = driver.FindElement(By.ClassName("inventory_item_name")).Text;
        Assert.Equal("Sauce Labs Backpack", cartItemName);

        driver.FindElement(By.Id("checkout")).Click();
        IWebElement checkoutPageElement = driver.FindElement(By.Id("checkout_info_container"));
        wait.Until(SeleniumExtras.WaitHelpers.ExpectedConditions.ElementIsVisible(By.Id("checkout_info_container")));

        driver.FindElement(By.Id("first-name")).SendKeys("John");
        driver.FindElement(By.Id("last-name")).SendKeys("Doe");
        driver.FindElement(By.Id("postal-code")).SendKeys("10001");
        driver.FindElement(By.Id("continue")).Click();

        string checkoutItemName = driver.FindElement(By.ClassName("inventory_item_name")).Text;
        Assert.Equal("Sauce Labs Backpack", checkoutItemName);

        driver.FindElement(By.Id("finish")).Click();

        bool successIsDisplayed = driver.FindElement(By.Id("checkout_complete_container")).Displayed;
        Assert.True(successIsDisplayed);

        driver.Quit();
    }
}
