using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Interactions;
using OpenQA.Selenium.Support.UI;
using System;
using Xunit;

public class DemoQATest
{
    private void ScrollPastElement(IWebDriver driver, IWebElement element)
    {
        new Actions(driver).MoveToElement(element).Perform();
    }

    // [Fact]
    public void Test()
    {
        string username = "research_paper";
        string password = "1tq52rw43E!";

        ChromeOptions options = new ChromeOptions();
        //options.AddArgument("--headless=new");
        IWebDriver driver = new ChromeDriver(options);
        driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(4);
        driver.Manage().Window.Size = new System.Drawing.Size(1920, 1080);
        WebDriverWait wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));

        try
        {
            driver.Navigate().GoToUrl("https://demoqa.com/login");
            driver.FindElement(By.Id("userName")).SendKeys(username);
            driver.FindElement(By.Id("password")).SendKeys(password);
            driver.FindElement(By.Id("login")).Click();

            var storeButton = driver.FindElement(By.Id("gotoStore"));
            ScrollPastElement(driver, storeButton);
            storeButton.Click();

            driver.FindElement(By.Id("see-book-Git Pocket Guide")).Click();
            string bookName = driver.FindElement(By.CssSelector("#title-wrapper #userName-value")).Text;

            var addNewRecordButton = driver.FindElement(By.Id("addNewRecordButton"));
            addNewRecordButton.Click();

            var profileButton = driver.FindElement(By.CssSelector(".show #item-3"));
            ScrollPastElement(driver, profileButton);
            profileButton.Click();

            var profileElement = driver.FindElement(By.Id("books-wrapper"));
            wait.Until(driver => driver.FindElement(By.Id("books-wrapper")).Displayed);

            driver.FindElement(By.Id("see-book-Git Pocket Guide")).Click();
            string firstRowTitleText = driver.FindElement(By.CssSelector("#title-wrapper #userName-value")).Text;
            Assert.Equal(firstRowTitleText, bookName);

            driver.Navigate().Back();
            driver.FindElement(By.Id("delete-record-undefined")).Click();
        }
        finally
        {
            driver.Quit();
        }
    }
}
