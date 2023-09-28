import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.interactions.WheelInput;
import org.openqa.selenium.support.ui.Wait;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

import static org.junit.Assert.assertEquals;

public class DemoQATest {
    private void scrollPastElement(WebDriver driver, WebElement element) {
	WheelInput.ScrollOrigin scrollOrigin = WheelInput.ScrollOrigin.fromElement(element);
	new Actions(driver).scrollFromOrigin(scrollOrigin, 0, 200).perform();
    }

    @Test
    public void test() {
        final String USERNAME = "research_paper";
        final String PASSWORD = "1tq52rw43E!";

	ChromeOptions options = new ChromeOptions();
	options.addArguments("--headless=new");
        WebDriver driver = new ChromeDriver(options);
        driver.manage().timeouts().implicitlyWait(Duration.ofMillis(4000));
        Wait<WebDriver> wait = new WebDriverWait(driver, Duration.ofSeconds(10));

        // Load the login page
        driver.get("https://demoqa.com/login");

        // Input username and password, click login button
        driver.findElement(By.id("userName")).sendKeys(USERNAME);
        driver.findElement(By.id("password")).sendKeys(PASSWORD);
        driver.findElement(By.id("login")).click();

        // Click "Go to Store" button
	WebElement storeButton = driver.findElement(By.id("gotoStore"));
	scrollPastElement(driver, storeButton);
        storeButton.click();

        // Click on the first book title
        driver.findElement(By.id("see-book-Git Pocket Guide")).click();

        // Store the name of the book
        String bookName = driver.findElement(By.cssSelector("#title-wrapper #userName-value")).getText();

        // Add the book to the collection
	WebElement addNewRecordButton = driver.findElement(By.id("addNewRecordButton"));
        addNewRecordButton.click();

        // Click profile button
	WebElement profileButton = driver.findElement(By.cssSelector(".show #item-3"));
	scrollPastElement(driver, profileButton);
        profileButton.click();

        // Wait until the profile page is loaded. This takes a while.
        WebElement profileElement = driver.findElement(By.id("books-wrapper"));
        wait.until(d -> profileElement.isDisplayed());

        // Click on the first book in the profile table
        driver.findElement(By.id("see-book-Git Pocket Guide")).click();

        // Get the book title and compare it to the stored value
        String firstRowTitleText = driver.findElement(By.cssSelector("#title-wrapper #userName-value")).getText();
        assertEquals(firstRowTitleText, bookName);

        // Go back to the profile page and delete the book.
        driver.navigate().back();
        driver.findElement(By.id("delete-record-undefined")).click();

        driver.close();
    }
}
