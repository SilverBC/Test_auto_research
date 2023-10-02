import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.Wait;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class CommerceTest {
    @Test
    public void test() {
	final String USERNAME = "standard_user";
	final String PASSWORD = "secret_sauce";

	Dimension dimension = new Dimension(1920, 1080);
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new");
        WebDriver driver = new ChromeDriver(options);
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(4));
        driver.manage().window().setSize(dimension);
        Wait<WebDriver> wait = new WebDriverWait(driver, Duration.ofSeconds(10));

        driver.get("https://www.saucedemo.com");

        driver.findElement(By.id("user-name")).sendKeys(USERNAME);
        driver.findElement(By.id("password")).sendKeys(PASSWORD);
        driver.findElement(By.id("login-button")).click();

        driver.findElement(By.id("add-to-cart-sauce-labs-backpack")).click();

        driver.findElement(By.id("shopping_cart_container")).click();

        WebElement cartPageElement = driver.findElement(By.className("cart_list"));
        wait.until(d -> cartPageElement.isDisplayed());

	String cartItemName = driver.findElement(By.className("inventory_item_name")).getText();
	assertEquals(cartItemName, "Sauce Labs Backpack");

	driver.findElement(By.id("checkout")).click();
	WebElement checkoutPageElement = driver.findElement(By.id("checkout_info_container"));
	wait.until(d -> checkoutPageElement.isDisplayed());

	driver.findElement(By.id("first-name")).sendKeys("John");
	driver.findElement(By.id("last-name")).sendKeys("Doe");
	driver.findElement(By.id("postal-code")).sendKeys("10001");
	driver.findElement(By.id("continue")).click();

	String checkoutItemName = driver.findElement(By.className("inventory_item_name")).getText();
	assertEquals(checkoutItemName, "Sauce Labs Backpack");

	driver.findElement(By.id("finish")).click();

	boolean successIsDisplayed = driver.findElement(By.id("checkout_complete_container")).isDisplayed();
	assertTrue(successIsDisplayed);
    }
}
